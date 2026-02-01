from gemini_deep_research_mcp.extract import interaction_to_result, outputs_to_text


def test_outputs_to_text_joins_text_fields() -> None:
    outputs = [
        {"type": "text", "text": "Hello"},
        {"type": "text", "text": "World"},
        {"type": "tool", "text": ""},
        {"type": "text", "text": "  "},
    ]
    # Disable citations to avoid HTTP resolution in tests
    assert outputs_to_text(outputs, include_citations=False) == "Hello\n\nWorld"


def test_interaction_to_result_returns_status_and_text() -> None:
    interaction = {
        "status": "completed",
        "outputs": [
            {
                "type": "text",
                "text": "Hello",
            }
        ],
    }
    # Disable citations to avoid HTTP resolution in tests
    result = interaction_to_result(interaction, include_citations=False)
    assert result["status"] == "completed"
    assert result["text"] == "Hello"
