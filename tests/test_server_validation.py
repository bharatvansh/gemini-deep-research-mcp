import pytest

from gemini_deep_research_mcp import server


def test_start_deep_research_requires_prompt() -> None:
    with pytest.raises(ValueError, match=r"`prompt` is required"):
        server.start_deep_research(prompt="")


def test_start_deep_research_requires_nonempty_prompt() -> None:
    with pytest.raises(ValueError, match=r"`prompt` is required"):
        server.start_deep_research(prompt="   ")


def test_check_deep_research_requires_job_id() -> None:
    with pytest.raises(ValueError, match=r"`job_id` is required"):
        server.check_deep_research(job_id="")


def test_check_deep_research_requires_nonempty_job_id() -> None:
    with pytest.raises(ValueError, match=r"`job_id` is required"):
        server.check_deep_research(job_id="   ")


def test_check_deep_research_missing_job_raises_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        server,
        "_get_client_and_settings",
        lambda: (
            object(),
            server.Settings(api_key="x", model="m", deep_research_agent="agent", poll_interval_seconds=1.0),
        ),
    )
    monkeypatch.setattr(server, "get_interaction", lambda _client, *, job_id: None)

    with pytest.raises(ValueError, match=r"No research job found for ID: nonexistent_id"):
        server.check_deep_research(job_id="nonexistent_id")
