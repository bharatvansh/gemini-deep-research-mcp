from __future__ import annotations

import logging
import sys
from typing import Annotated, Any, TypedDict

from mcp.server.fastmcp import FastMCP
from mcp.types import CallToolResult, ToolAnnotations

from .config import Settings, load_settings
from .extract import interaction_to_result
from .gemini import create_client, poll_until_terminal, start_deep_research


logger = logging.getLogger(__name__)


class DeepResearchOutput(TypedDict):
    interaction_id: str
    status: str
    report_text: str
    citations: list[dict[str, Any]]


def _configure_logging() -> None:
    # IMPORTANT: stdout is reserved for MCP protocol.
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
        stream=sys.stderr,
    )


_configure_logging()


mcp = FastMCP("Gemini Deep Research MCP")


def _get_client_and_settings() -> tuple[Any, Settings]:
    settings = load_settings()
    client = create_client(settings)
    return client, settings


def _require_nonempty(value: Optional[str], *, field: str) -> str:
    if value is None:
        raise ValueError(f"`{field}` is required")
    value = str(value)
    if not value.strip():
        raise ValueError(f"`{field}` is required")
    return value


_DEEP_RESEARCH_DESCRIPTION = """
Conduct comprehensive web research using Gemini's Deep Research Agent.

When to use this tool:
- Researching complex topics requiring multi-source analysis
- Need synthesized information with citations from the web
- Require fact-checking and cross-referencing of information

Parameters:
- `prompt`: Your research question or topic (required)
- `timeout_seconds`: Max time to wait for completion (default: 900 seconds)

Returns:
- `interaction_id`: Unique identifier for this research
- `status`: Final state (completed, failed, cancelled)
- `report_text`: The synthesized research report with findings
- `citations`: List of source citations

Notes:
- This tool blocks until research completes (typically 10-20 minutes)
""".strip()


@mcp.tool(
    title="Gemini Deep Research",
    description=_DEEP_RESEARCH_DESCRIPTION,
    annotations=ToolAnnotations(
        openWorldHint=True,
        readOnlyHint=False,
        idempotentHint=False,
    ),
    structured_output=True,
)
def gemini_deep_research(
    prompt: str,
    timeout_seconds: float = 900,
) -> Annotated[CallToolResult, DeepResearchOutput]:
    """Conduct deep research on a topic and wait for the complete report."""

    if not prompt or not prompt.strip():
        raise ValueError("`prompt` is required")
    if timeout_seconds <= 0:
        raise ValueError("`timeout_seconds` must be > 0")

    client, settings = _get_client_and_settings()

    # Start the deep research job
    initial = start_deep_research(client, prompt=prompt.strip(), agent=settings.deep_research_agent)
    interaction_id = getattr(initial, "id", None) or (
        initial.get("id") if isinstance(initial, dict) else None
    )
    if not interaction_id:
        raise RuntimeError("Gemini SDK did not return an interaction id.")

    # Wait for completion
    interaction = poll_until_terminal(
        client,
        interaction_id=interaction_id,
        timeout_seconds=timeout_seconds,
        poll_interval_seconds=settings.poll_interval_seconds,
    )
    result = interaction_to_result(interaction)
    status = result.get("status")
    if status is None:
        status = "unknown"
    payload: DeepResearchOutput = {
        "interaction_id": result.get("interaction_id") or interaction_id,
        "status": str(status),
        "report_text": result.get("text", ""),
        "citations": result.get("citations", []),
    }

    # IMPORTANT: when returning a dict from a structured tool, the MCP lowlevel server
    # will also serialize it to JSON text and include it in `content`, which some
    # clients then print in addition to `structuredContent` (leading to duplicate
    # outputs). Returning CallToolResult avoids that double-serialization.
    return CallToolResult(content=[], structuredContent=payload, isError=False)





def main() -> None:
    # Run over STDIO.
    logger.info("Starting Gemini Deep Research MCP server (stdio)")
    mcp.run()
