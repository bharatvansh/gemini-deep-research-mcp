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


_DEEP_RESEARCH_DESCRIPTION = (
    "Start a Gemini Deep Research interaction (Deep Research Agent) OR poll an existing interaction.\n\n"
    "Provide EXACTLY ONE of: `prompt` (to start) or `interaction_id` (to poll). Do not provide both.\n\n"
    "Typical usage:\n"
    "- Start: set `prompt`, set `wait=false` to get an interaction id quickly.\n"
    "- Poll: call again with `interaction_id`; set `wait=true` to block until a terminal status or timeout.\n\n"
    "Notes:\n"
    "- When `wait=true`, `timeout_seconds` must be > 0 and controls polling duration.\n"
    "- `status` is the raw Gemini interaction status string; terminal statuses are usually: completed/failed/cancelled.\n"
    "- `citations` is best-effort extraction from output annotations and may vary by model/agent response format."
)


@mcp.tool(
    title="Gemini Deep Research",
    description=_DEEP_RESEARCH_DESCRIPTION,
    annotations=ToolAnnotations(openWorldHint=True),
    structured_output=True,
)
def gemini_deep_research(
    prompt: Optional[str] = None,
    interaction_id: Optional[str] = None,
    wait: bool = True,
    timeout_seconds: float = 600,
) -> Dict[str, Any]:
    """Start or poll a Gemini Deep Research interaction.

    This tool has two mutually-exclusive modes:

    1) Start mode: provide `prompt`.
    2) Poll mode: provide `interaction_id`.
    """

    prompt_is_set = prompt is not None and str(prompt).strip() != ""
    interaction_is_set = interaction_id is not None and str(interaction_id).strip() != ""

    if prompt_is_set and interaction_is_set:
        raise ValueError("Provide exactly one of `prompt` or `interaction_id` (not both).")
    if not prompt_is_set and not interaction_is_set:
        raise ValueError("Provide exactly one of `prompt` or `interaction_id`.")
    if wait and timeout_seconds <= 0:
        raise ValueError("`timeout_seconds` must be > 0 when `wait=true`.")

    client, settings = _get_client_and_settings()

    if interaction_is_set:
        interaction_id = _require_nonempty(interaction_id, field="interaction_id")
        # Resume/poll an existing interaction.
        if wait:
            interaction = poll_until_terminal(
                client,
                interaction_id=interaction_id,
                timeout_seconds=timeout_seconds,
                poll_interval_seconds=settings.poll_interval_seconds,
            )
        else:
            interaction = client.interactions.get(interaction_id)

        result = interaction_to_result(interaction)
        return {
            "interaction_id": result.get("interaction_id") or interaction_id,
            "status": result.get("status"),
            "report_text": result.get("text", ""),
            "citations": result.get("citations", []),
        }

    prompt = _require_nonempty(prompt, field="prompt")

    # Start a new deep research job.
    initial = start_deep_research(client, prompt=prompt, agent=settings.deep_research_agent)
    new_id = getattr(initial, "id", None) or (
        initial.get("id") if isinstance(initial, dict) else None
    )
    if not new_id:
        # Shouldn't happen, but keep it explicit.
        raise RuntimeError("Gemini SDK did not return an interaction id.")

    if not wait:
        result = interaction_to_result(initial)
        return {
            "interaction_id": new_id,
            "status": result.get("status"),
            "report_text": result.get("text", ""),
            "citations": result.get("citations", []),
        }

    interaction = poll_until_terminal(
        client,
        interaction_id=new_id,
        timeout_seconds=timeout_seconds,
        poll_interval_seconds=settings.poll_interval_seconds,
    )
    result = interaction_to_result(interaction)
    return {
        "interaction_id": result.get("interaction_id") or new_id,
        "status": result.get("status"),
        "report_text": result.get("text", ""),
        "citations": result.get("citations", []),
    }


@mcp.tool(
    name="gemini-deep-research",
    title="Gemini Deep Research",
    description=(
        _DEEP_RESEARCH_DESCRIPTION
        + "\n\nCompatibility: this is an alias of `gemini_deep_research` with a kebab-case tool name."
    ),
    annotations=ToolAnnotations(openWorldHint=True),
    structured_output=True,
)
def gemini_deep_research_alias(
    prompt: Optional[str] = None,
    interaction_id: Optional[str] = None,
    wait: bool = True,
    timeout_seconds: float = 600,
) -> Dict[str, Any]:
    """Alias for `gemini_deep_research` (kebab-case name)."""

    return gemini_deep_research(
        prompt=prompt,
        interaction_id=interaction_id,
        wait=wait,
        timeout_seconds=timeout_seconds,
    )


@mcp.tool(
    title="Gemini Deep Research Follow-up",
    description=(
        "Ask a follow-up question about an existing research interaction.\n\n"
        "Inputs:\n"
        "- `previous_interaction_id`: the prior interaction id to use as context (required).\n"
        "- `question`: the follow-up question to ask (required).\n"
        "- `model`: optional Gemini model id override; defaults to GEMINI_MODEL.\n\n"
        "Notes:\n"
        "- This creates a new interaction linked to the previous one (store=true).\n"
        "- Returns best-effort extracted citations from output annotations."
    ),
    annotations=ToolAnnotations(openWorldHint=True),
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


@mcp.tool(
    name="gemini-deep-research-followup",
    title="Gemini Deep Research Follow-up",
    description=(
        "Alias of `gemini_deep_research_followup` with a kebab-case tool name.\n\n"
        "Use this to ask follow-up questions about a previous deep research interaction."
    ),
    annotations=ToolAnnotations(openWorldHint=True),
    structured_output=True,
)
def gemini_deep_research_followup_alias(
    previous_interaction_id: str,
    question: str,
    model: Optional[str] = None,
) -> Dict[str, Any]:
    """Alias for `gemini_deep_research_followup` (kebab-case name)."""

    return gemini_deep_research_followup(
        previous_interaction_id=previous_interaction_id,
        question=question,
        model=model,
    )


def main() -> None:
    # Run over STDIO.
    logger.info("Starting Gemini Deep Research MCP server (stdio)")
    mcp.run()
