from __future__ import annotations

from typing import Any

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
