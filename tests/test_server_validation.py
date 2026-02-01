import pytest

from gemini_deep_research_mcp import server


def test_gemini_deep_research_requires_prompt() -> None:
    with pytest.raises(ValueError, match=r"`prompt` is required"):
        server.gemini_deep_research(prompt="")


def test_gemini_deep_research_requires_nonempty_prompt() -> None:
    with pytest.raises(ValueError, match=r"`prompt` is required"):
        server.gemini_deep_research(prompt="   ")


def test_gemini_deep_research_timeout_must_be_positive() -> None:
    with pytest.raises(ValueError, match=r"`timeout_seconds` must be > 0"):
        server.gemini_deep_research(prompt="test", timeout_seconds=0)


def test_gemini_deep_research_negative_timeout_rejected() -> None:
    with pytest.raises(ValueError, match=r"`timeout_seconds` must be > 0"):
        server.gemini_deep_research(prompt="test", timeout_seconds=-10)


def test_followup_requires_previous_interaction_id() -> None:
    with pytest.raises(ValueError, match=r"`previous_interaction_id` is required"):
        server.gemini_deep_research_followup(previous_interaction_id="", question="hi")


def test_followup_requires_question() -> None:
    with pytest.raises(ValueError, match=r"`question` is required"):
        server.gemini_deep_research_followup(previous_interaction_id="abc", question="")
