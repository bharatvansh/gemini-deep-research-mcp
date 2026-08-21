from types import SimpleNamespace

from gemini_deep_research_mcp.gemini import get_interaction


def test_get_interaction_calls_interactions_get() -> None:
    expected = {"id": "int_1", "status": "in_progress"}

    client = SimpleNamespace(
        interactions=SimpleNamespace(
            get=lambda job_id: expected if job_id == "int_1" else None
        )
    )

    assert get_interaction(client, "int_1") == expected

