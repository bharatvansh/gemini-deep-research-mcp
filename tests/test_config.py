import pytest

from gemini_deep_research_mcp.config import Settings, load_settings


def test_load_settings_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_DEEP_RESEARCH_AGENT", raising=False)

    settings = load_settings()
    assert isinstance(settings, Settings)
    assert settings.api_key == ""
    assert settings.deep_research_agent == "deep-research-preview-04-2026"


def test_load_settings_with_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "test_key_123")
    monkeypatch.setenv("GEMINI_DEEP_RESEARCH_AGENT", "deep-research-max-preview-04-2026")

    settings = load_settings()
    assert settings.api_key == "test_key_123"
    assert settings.deep_research_agent == "deep-research-max-preview-04-2026"


def test_load_settings_google_api_key_fallback(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.setenv("GOOGLE_API_KEY", "google_test_key")

    settings = load_settings()
    assert settings.api_key == "google_test_key"
