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


def _finalize_text(text: str, *, include_citations: bool) -> str:
    result = _strip_duplicate_references(text.strip())
    if include_citations:
        result = resolve_sources_in_text(result)
    return result


def outputs_to_text(outputs: Optional[Iterable[Any]], *, include_citations: bool = True) -> str:
    """Best-effort conversion of text-bearing output items to readable text."""

    if not outputs:
        return ""

    parts: List[str] = []
    for out in outputs:
        text = _get(out, "text")
        if isinstance(text, str) and text.strip():
            parts.append(text)
    
    return _finalize_text("\n\n".join(parts), include_citations=include_citations)


def _step_text_content(steps: Optional[Iterable[Any]]) -> Iterable[Any]:
    """Yield text-bearing content from modern Interaction model output steps."""
    if not steps:
        return
    for step in steps:
        if _get(step, "type") != "model_output":
            continue
        content = _get(step, "content")
        if content:
            yield from content


def interaction_to_result(interaction: Any, *, include_citations: bool = True) -> dict[str, Any]:
    """Convert an Interaction object to a JSON-serializable summary."""

    outputs = _get(interaction, "outputs")
    if outputs:
        text = outputs_to_text(outputs, include_citations=include_citations)
    else:
        # Current google-genai Interaction objects expose `steps` and the
        # convenience `output_text` property instead of the legacy `outputs`
        # field. Prefer the SDK property, while retaining dict compatibility.
        output_text = _get(interaction, "output_text")
        if isinstance(output_text, str):
            text = _finalize_text(output_text, include_citations=include_citations)
        else:
            text = outputs_to_text(
                _step_text_content(_get(interaction, "steps")),
                include_citations=include_citations,
            )

    return {
        "status": _get(interaction, "status"),
        "text": text,
    }
