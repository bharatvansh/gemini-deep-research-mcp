from gemini_deep_research_mcp.extract import (
    interaction_to_result,
    outputs_to_citations,
    outputs_to_text,
    sources_from_report_text,
)


def test_outputs_to_text_joins_text_fields() -> None:
    outputs = [
        {"type": "text", "text": "Hello"},
        {"type": "text", "text": "World"},
        {"type": "tool", "text": ""},
        {"type": "text", "text": "  "},
    ]
    assert outputs_to_text(outputs) == "Hello\n\nWorld"


def test_outputs_to_citations_extracts_annotations() -> None:
    outputs = [
        {
            "type": "text",
            "text": "Answer",
            "annotations": [
                {
                    "type": "citation",
                    "url": "https://example.com",
                    "title": "Example",
                }
            ],
        }
    ]
    citations = outputs_to_citations(outputs)
    assert len(citations) == 1
    assert citations[0]["url"] == "https://example.com"


def test_outputs_to_citations_drops_span_only_citations() -> None:
    outputs = [
        {
            "type": "text",
            "text": "Hello [cite: 1]",
            "annotations": [
                {
                    "type": "citation",
                    "start_index": 6,
                    "end_index": 15,
                }
            ],
        }
    ]
    assert outputs_to_citations(outputs) == []


def test_sources_from_report_text_parses_markdown_links() -> None:
    text = """Title\n\n**Sources:**\n1. [example.com](https://example.com)\n2. [foo](https://foo.bar)\n"""
    sources = sources_from_report_text(text)
    assert len(sources) == 2
    assert sources[0]["index"] == 1
    assert sources[0]["title"] == "example.com"
    assert sources[0]["url"] == "https://example.com"


def test_interaction_to_result_falls_back_to_sources_list() -> None:
    interaction = {
        "id": "int1",
        "status": "completed",
        "outputs": [
            {
                "type": "text",
                "text": """Hello\n\n**Sources:**\n1. [example.com](https://example.com)\n""",
                "annotations": [
                    {"type": "citation", "start_index": 0, "end_index": 5}
                ],
            }
        ],
    }
    result = interaction_to_result(interaction)
    assert result["citations"] == [{"index": 1, "title": "example.com", "url": "https://example.com"}]
