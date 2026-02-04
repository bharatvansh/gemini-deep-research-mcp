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
    status: str
    report_text: str


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


# Default timeout for research
_DEFAULT_TIMEOUT_SECONDS = 1200.0

_DEEP_RESEARCH_DESCRIPTION = """
Conduct comprehensive web research using a Deep Research Agent.

When to use this tool:
- Researching complex topics requiring multi-source analysis
- Need synthesized information from the web
- Require fact-checking and cross-referencing of information

Parameters:
- `prompt`: Your research question or topic (required)
- `include_citations`: Whether to include source URLs in the report (default: true)

Returns:
- `status`: Final state (completed, failed, cancelled)
- `report_text`: The synthesized research report with findings
- `sources`: List of sources used in the research (if enabled)

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
    include_citations: bool = True,
) -> Annotated[CallToolResult, DeepResearchOutput]:
    """Conduct deep research on a topic and wait for the complete report."""

    if not prompt or not prompt.strip():
        raise ValueError("`prompt` is required")

    client, settings = _get_client_and_settings()

    # Start the deep research job
    initial = start_deep_research(client, prompt=prompt.strip(), agent=settings.deep_research_agent)
    job_id = getattr(initial, "id", None) or (
        initial.get("id") if isinstance(initial, dict) else None
    )
    if not job_id:
        raise RuntimeError("Gemini SDK did not return a research job id.")

    # Wait for completion
    interaction = poll_until_terminal(
        client,
        job_id=job_id,
        timeout_seconds=_DEFAULT_TIMEOUT_SECONDS,
        poll_interval_seconds=settings.poll_interval_seconds,
    )
    result = interaction_to_result(interaction, include_citations=include_citations)
    status = result.get("status")
    if status is None:
        status = "unknown"
    payload: DeepResearchOutput = {
        "status": str(status),
        "report_text": result.get("text", ""),
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
