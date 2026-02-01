import pytest

from gemini_deep_research_mcp import server


def test_gemini_deep_research_requires_prompt() -> None:
    with pytest.raises(ValueError, match=r"`prompt` is required"):
        server.gemini_deep_research(prompt="")


def test_gemini_deep_research_requires_nonempty_prompt() -> None:
    with pytest.raises(ValueError, match=r"`prompt` is required"):
        server.gemini_deep_research(prompt="   ")
