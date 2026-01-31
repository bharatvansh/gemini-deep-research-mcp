from gemini_deep_research_mcp.extract import outputs_to_citations, outputs_to_text


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
