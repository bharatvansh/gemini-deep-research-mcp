from __future__ import annotations

import logging
import sys
from typing import Any, Dict, Literal, Optional

from mcp.server.fastmcp import FastMCP

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


@mcp.tool()
def gemini_deep_research(
    prompt: Optional[str] = None,
    interaction_id: Optional[str] = None,
    wait: bool = True,
    timeout_seconds: float = 600,
) -> Dict[str, Any]:
    """Start a new Gemini Deep Research interaction (using the Deep Research Agent), or poll an existing one."""

    client, settings = _get_client_and_settings()

    if interaction_id:
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

    if not prompt or not str(prompt).strip():
        raise ValueError("`prompt` is required when `interaction_id` is not provided.")

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


@mcp.tool()
def gemini_deep_research_followup(
    previous_interaction_id: str,
    question: str,
    model: Literal["flash", "pro"] = "pro",
) -> Dict[str, Any]:
    """Ask a follow-up question regarding a research interaction, using Gemini 3 Flash or Pro models."""

    if not previous_interaction_id or not previous_interaction_id.strip():
        raise ValueError("`previous_interaction_id` is required")
    if not question or not question.strip():
        raise ValueError("`question` is required")

    client, settings = _get_client_and_settings()
    model_id = settings.pro_model if model == "pro" else settings.flash_model

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
