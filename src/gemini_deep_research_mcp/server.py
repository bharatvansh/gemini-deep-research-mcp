from __future__ import annotations

import logging
import sys
from typing import Any, Dict, Literal, Optional

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from .config import Settings, load_settings
from .extract import interaction_to_result
from .gemini import create_client, followup, poll_until_terminal, start_deep_research


logger = logging.getLogger(__name__)


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
- `interaction_id`: Unique identifier for this research (use with follow-up tool)
- `status`: Final state (completed, failed, cancelled)
- `report_text`: The synthesized research report with findings
- `citations`: List of source citations

Notes:
- This tool blocks until research completes (typically 10-20 minutes)
- For follow-up questions, use the `gemini_deep_research_followup` tool with the returned `interaction_id`
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
) -> Dict[str, Any]:
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
    return {
        "interaction_id": result.get("interaction_id") or interaction_id,
        "status": result.get("status"),
        "report_text": result.get("text", ""),
        "citations": result.get("citations", []),
    }


_FOLLOWUP_DESCRIPTION = """
Ask follow-up questions about a completed research interaction, using the original research as context.

When to use this tool:
- Clarifying specific points from a research report
- Drilling deeper into a particular aspect of the research
- Asking related questions that build on previous findings
- Requesting additional analysis, comparisons, or explanations

Required Parameters:
- `previous_interaction_id`: The interaction ID from a completed `gemini_deep_research` call
- `question`: Your follow-up question

Optional Parameters:
- `model`: Override the Gemini model (e.g., 'gemini-3-pro-preview', 'gemini-3-flash-preview')
  - Pro: Higher quality, more thorough responses
  - Flash: Faster responses, good for simple clarifications
  - Defaults to GEMINI_MODEL environment variable

Returns:
- `interaction_id`: New interaction ID for this follow-up
- `answer_text`: The AI's response to your question
- `citations`: Any additional citations referenced in the answer

Notes:
- You must only use this tool after completing a `gemini_deep_research` interaction.
""".strip()


@mcp.tool(
    title="Gemini Deep Research Follow-up",
    description=_FOLLOWUP_DESCRIPTION,
    annotations=ToolAnnotations(
        openWorldHint=True,
        readOnlyHint=True,
        idempotentHint=True,
    ),
    structured_output=True,
)
def gemini_deep_research_followup(
    previous_interaction_id: str,
    question: str,
    model: Optional[str] = None,
) -> Dict[str, Any]:
    """Ask a follow-up question regarding a research interaction.
    
    Args:
        previous_interaction_id: The ID of the research to follow up on.
        question: Your question.
        model: Optional model override (e.g. 'gemini-3-pro-preview' or 'gemini-3-flash-preview').
               Defaults to the configured GEMINI_MODEL.
    """

    if not previous_interaction_id or not previous_interaction_id.strip():
        raise ValueError("`previous_interaction_id` is required")
    if not question or not question.strip():
        raise ValueError("`question` is required")

    client, settings = _get_client_and_settings()
    model_id = model or settings.model

    interaction = followup(
        client,
        previous_interaction_id=previous_interaction_id,
        question=question,
        model=model_id,
    )
    result = interaction_to_result(interaction)
    return {
        "interaction_id": result.get("interaction_id"),
        "answer_text": result.get("text", ""),
        "citations": result.get("citations", []),
    }


def main() -> None:
    # Run over STDIO.
    logger.info("Starting Gemini Deep Research MCP server (stdio)")
    mcp.run()
