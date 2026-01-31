import pytest

from gemini_deep_research_mcp import server


def test_gemini_deep_research_requires_exactly_one_mode_arg() -> None:
    with pytest.raises(ValueError, match=r"exactly one of `prompt` or `interaction_id`"):
        server.gemini_deep_research(prompt=None, interaction_id=None)


def test_gemini_deep_research_rejects_both_mode_args() -> None:
    with pytest.raises(ValueError, match=r"exactly one of `prompt` or `interaction_id`"):
        server.gemini_deep_research(prompt="test", interaction_id="abc")


def test_gemini_deep_research_timeout_must_be_positive_when_waiting() -> None:
    with pytest.raises(ValueError, match=r"timeout_seconds"):
        server.gemini_deep_research(prompt="test", wait=True, timeout_seconds=0)


def test_followup_requires_previous_interaction_id() -> None:
    with pytest.raises(ValueError, match=r"previous_interaction_id"):
        server.gemini_deep_research_followup(previous_interaction_id="", question="hi")


def test_followup_requires_question() -> None:
    with pytest.raises(ValueError, match=r"`question` is required"):
        server.gemini_deep_research_followup(previous_interaction_id="abc", question="")
