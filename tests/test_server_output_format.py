import pytest

from mcp.types import CallToolResult

from mcp.server.fastmcp.tools.base import Tool

from gemini_deep_research_mcp import server


def test_deep_research_returns_structured_only(monkeypatch: pytest.MonkeyPatch) -> None:
    """Regression: avoid duplicate JSON output by returning CallToolResult.

    The MCP lowlevel server serializes structured dict outputs to JSON text and also
    returns them as structuredContent. Some clients then print both.
    """

    monkeypatch.setattr(
        server,
        "_get_client_and_settings",
        lambda: (
            object(),
            server.Settings(api_key="x", model="m", deep_research_agent="agent", poll_interval_seconds=1.0),
        ),
    )
    monkeypatch.setattr(server, "start_deep_research", lambda _client, *, prompt, agent: {"id": "int1"})
    monkeypatch.setattr(server, "poll_until_terminal", lambda *_args, **_kwargs: object())
    monkeypatch.setattr(
        server,
        "interaction_to_result",
        lambda _interaction: {
            "status": "completed",
            "text": "REPORT",
        },
    )

    result = server.gemini_deep_research(prompt="test", timeout_seconds=1)
    assert isinstance(result, CallToolResult)

    # Critical: avoid JSON-serialized duplicate output in `content`.
    assert result.content == []
    assert result.isError is False
    assert result.structuredContent is not None
    assert result.structuredContent["status"] == "completed"
    assert result.structuredContent["report_text"] == "REPORT"


def test_deep_research_fastmcp_validation_accepts_structured_content(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Exercises FastMCP convert_result validation.

    This catches regressions where the output schema expects a wrapped
    {"result": ...} shape and rejects our structuredContent.
    """

    monkeypatch.setattr(
        server,
        "_get_client_and_settings",
        lambda: (
            object(),
            server.Settings(api_key="x", model="m", deep_research_agent="agent", poll_interval_seconds=1.0),
        ),
    )
    monkeypatch.setattr(server, "start_deep_research", lambda _client, *, prompt, agent: {"id": "int1"})
    monkeypatch.setattr(server, "poll_until_terminal", lambda *_args, **_kwargs: object())
    monkeypatch.setattr(
        server,
        "interaction_to_result",
        lambda _interaction: {
            "status": "completed",
            "text": "REPORT",
        },
    )

    tool = Tool.from_function(server.gemini_deep_research, structured_output=True)

    # Tool.run is async; use a local event loop without extra deps.
    import asyncio

    result = asyncio.run(tool.run({"prompt": "test", "timeout_seconds": 1}, convert_result=True))
    assert isinstance(result, CallToolResult)
    assert result.structuredContent is not None
    assert result.structuredContent["report_text"] == "REPORT"