from __future__ import annotations

import time
from typing import Any, Optional

from google import genai

from .config import Settings


def create_client(settings: Settings) -> genai.Client:
    # The SDK supports GOOGLE_API_KEY env var, but we pass explicitly for clarity.
    if not settings.api_key:
        raise ValueError(
            "Missing GEMINI_API_KEY (or GOOGLE_API_KEY fallback). "
            "Set it in your environment or .env."
        )
    return genai.Client(api_key=settings.api_key)


def start_deep_research(client: genai.Client, *, prompt: str, agent: str) -> Any:
    # For Deep Research: background=True requires store=True.
    return client.interactions.create(
        input=prompt,
        agent=agent,
        background=True,
        store=True,
    )


def get_interaction(client: genai.Client, job_id: str) -> Any:
    return client.interactions.get(job_id)


def poll_until_terminal(
    client: genai.Client,
    *,
    job_id: str,
    timeout_seconds: float,
    poll_interval_seconds: float,
) -> Any:
    deadline = time.monotonic() + max(0.0, timeout_seconds)

    interaction: Optional[Any] = None
    while True:
        interaction = get_interaction(client, job_id)
        status = getattr(interaction, "status", None) or (
            interaction.get("status") if isinstance(interaction, dict) else None
        )

        if status in {"completed", "failed", "cancelled"}:
            return interaction

        if time.monotonic() >= deadline:
            return interaction

        time.sleep(poll_interval_seconds)
