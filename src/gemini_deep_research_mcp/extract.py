from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional


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


def _normalize_annotation(a: Any) -> Dict[str, Any]:
    if isinstance(a, dict):
        # Ensure it's JSON-serializable and keep useful keys.
        return dict(a)

    # Unknown object type — extract common fields if they exist.
    result: Dict[str, Any] = {}
    for k in (
        "type",
        "id",
        "url",
        "title",
        "start_index",
        "end_index",
        "cited_text",
        "extras",
    ):
        v = getattr(a, k, None)
        if v is not None:
            result[k] = v
    return result


def outputs_to_citations(outputs: Optional[Iterable[Any]]) -> List[Dict[str, Any]]:
    """Extract citation-like annotations from outputs.

    The Gemini Interactions API may return per-output `annotations` (e.g. citations
    from grounded results / web search). We return a list of dicts.
    """

    citations: List[Dict[str, Any]] = []
    if not outputs:
        return citations

    for out in outputs:
        annotations = _get(out, "annotations")
        if not annotations:
            continue
        for a in annotations:
            ann = _normalize_annotation(a)

            # Some schemas label citations explicitly.
            ann_type = ann.get("type")
            if ann_type and ann_type != "citation":
                # Still keep non-citation annotations if they look like sources.
                if not (ann.get("url") or ann.get("title")):
                    continue

            citations.append(ann)

    return citations


def interaction_to_result(interaction: Any) -> Dict[str, Any]:
    """Convert an Interaction object to a JSON-serializable summary."""

    outputs = _get(interaction, "outputs")
    return {
        "interaction_id": _get(interaction, "id"),
        "status": _get(interaction, "status"),
        "text": outputs_to_text(outputs),
        "citations": outputs_to_citations(outputs),
    }
