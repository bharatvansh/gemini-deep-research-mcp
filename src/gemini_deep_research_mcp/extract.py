from __future__ import annotations

from typing import Any, Iterable, List, Optional


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
    return "\n\n".join(parts).strip()


def interaction_to_result(interaction: Any) -> dict[str, Any]:
    """Convert an Interaction object to a JSON-serializable summary."""

    outputs = _get(interaction, "outputs")
    text = outputs_to_text(outputs)

    return {
        "status": _get(interaction, "status"),
        "text": text,
    }
