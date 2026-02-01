from __future__ import annotations

import re
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


def _dedupe_dicts(items: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Return items with duplicates removed (stable order).

    We dedupe by a deterministic string key built from common fields.
    """

    seen: set[str] = set()
    out: List[Dict[str, Any]] = []
    for it in items:
        key = "|".join(
            str(it.get(k, ""))
            for k in (
                "type",
                "id",
                "url",
                "title",
                "start_index",
                "end_index",
                "cited_text",
            )
        )
        if key in seen:
            continue
        seen.add(key)
        out.append(it)
    return out


_SOURCE_LINE_RE = re.compile(r"^\s*(\d+)\.\s*\[([^\]]+)\]\(([^)]+)\)\s*$", re.MULTILINE)


def sources_from_report_text(text: str) -> List[Dict[str, Any]]:
    """Extract a Sources list from the report text.

    Gemini Deep Research reports typically end with:

        **Sources:**
        1. [example.com](https://...)

    We parse those into a structured list.
    """

    if not text or not isinstance(text, str):
        return []

    matches = list(_SOURCE_LINE_RE.finditer(text))
    if not matches:
        return []

    sources: List[Dict[str, Any]] = []
    for m in matches:
        idx_s, title, url = m.group(1), m.group(2), m.group(3)
        try:
            idx = int(idx_s)
        except ValueError:
            idx = None
        sources.append({"index": idx, "title": title, "url": url})

    return _dedupe_dicts(sources)


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

            # Gemini sometimes returns citation annotations that only contain span
            # offsets (start_index/end_index) without any actual source info.
            # Those are not very useful on their own (and can be duplicated), so we
            # drop them here. If you need spans, consider extending the API to
            # return a separate `citation_spans` field.
            if ann_type == "citation" and not (ann.get("url") or ann.get("title") or ann.get("cited_text")):
                continue

            citations.append(ann)

    return _dedupe_dicts(citations)


def interaction_to_result(interaction: Any) -> Dict[str, Any]:
    """Convert an Interaction object to a JSON-serializable summary."""

    outputs = _get(interaction, "outputs")
    text = outputs_to_text(outputs)
    citations = outputs_to_citations(outputs)

    # If the SDK didn't give us source URLs/titles, fall back to parsing the
    # report's Sources section (common in Deep Research reports).
    if not any(c.get("url") or c.get("title") for c in citations):
        parsed_sources = sources_from_report_text(text)
        if parsed_sources:
            citations = parsed_sources

    return {
        "interaction_id": _get(interaction, "id"),
        "status": _get(interaction, "status"),
        "text": text,
        "citations": citations,
    }
