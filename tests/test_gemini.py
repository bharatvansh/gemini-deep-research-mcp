from types import SimpleNamespace
import pytest

from gemini_deep_research_mcp.config import Settings
from gemini_deep_research_mcp.gemini import create_client, get_interaction, start_deep_research


def test_create_client_raises_on_missing_api_key() -> None:
    settings = Settings(api_key="", deep_research_agent="agent")
    with pytest.raises(ValueError, match=r"Missing GEMINI_API_KEY"):
        create_client(settings)


def test_start_deep_research_calls_interactions_create() -> None:
    calls = []

    def mock_create(**kwargs):
        calls.append(kwargs)
        return {"id": "int_999", "status": "in_progress"}

    client = SimpleNamespace(
        interactions=SimpleNamespace(create=mock_create)
    )

    result = start_deep_research(client, prompt="Quantum Computing", agent="agent-preview")
    assert result == {"id": "int_999", "status": "in_progress"}
    assert len(calls) == 1
    assert calls[0] == {
        "input": "Quantum Computing",
        "agent": "agent-preview",
        "background": True,
        "store": True,
    }


def test_get_interaction_calls_interactions_get() -> None:
    expected = {"id": "int_1", "status": "in_progress"}

    client = SimpleNamespace(
        interactions=SimpleNamespace(
            get=lambda job_id: expected if job_id == "int_1" else None
        )
    )

    assert get_interaction(client, "int_1") == expected

