from __future__ import annotations

import re
from typing import Any, Iterable, List, Optional

from .resolve import resolve_sources_in_text


def _strip_duplicate_references(text: str) -> str:
    """Remove the redundant 'References' section while keeping 'Sources'.
    
    Gemini Deep Research reports contain:
    1. Inline [cite: X] markers throughout the text
    2. A 'References' section with brief citation titles (REDUNDANT)
    3. A 'Sources:' section at the end with full URLs (KEEP THIS)
    
    We remove the References section since:
    - The inline [cite: X] markers already show where info comes from
    - The Sources section has the actual clickable URLs
    - The References section just has brief titles without URLs
    
    This typically saves ~1-2KB per report.
    """
    # Match "### References" or "References" section with cite entries
    # Format: [cite: X] Title. Description.
    pattern = r'\n+(?:#{1,3}\s*)?References\s*\n(?:\[cite:\s*\d+\][^\n]*\n?)+'
    cleaned = re.sub(pattern, '\n', text, flags=re.IGNORECASE)
    return cleaned.strip()


def _get(obj: Any, key: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def outputs_to_text(outputs: Optional[Iterable[Any]]) -> str:
    """Best-effort conversion of Interaction.outputs to a readable string."""

    if not outputs:
        return ""

    parts: List[str] = []
    for out in outputs:
        text = _get(out, "text")
        if isinstance(text, str) and text.strip():
            parts.append(text)
    
    result = _strip_duplicate_references("\n\n".join(parts).strip())
    # Resolve redirect URLs to actual source URLs
    result = resolve_sources_in_text(result)
    return result


def interaction_to_result(interaction: Any) -> dict[str, Any]:
    """Convert an Interaction object to a JSON-serializable summary."""

    outputs = _get(interaction, "outputs")
    text = outputs_to_text(outputs)

    return {
        "status": _get(interaction, "status"),
        "text": text,
    }
