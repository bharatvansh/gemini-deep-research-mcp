from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    api_key: str
    model: str
    deep_research_agent: str
    poll_interval_seconds: float = 10.0


def load_settings() -> Settings:
    """Load configuration from environment (and .env when present)."""

    # Load .env if present; safe no-op otherwise.
    load_dotenv(override=False)

    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or ""

    model = os.getenv("GEMINI_MODEL", "gemini-3-pro-preview")
    deep_research_agent = os.getenv(
        "GEMINI_DEEP_RESEARCH_AGENT", "deep-research-pro-preview-12-2025"
    )

    return Settings(
        api_key=api_key,
        model=model,
        deep_research_agent=deep_research_agent,
    )
