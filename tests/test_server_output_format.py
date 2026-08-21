import asyncio
import pytest

from mcp.types import CallToolResult
from mcp.server.fastmcp.tools.base import Tool

from gemini_deep_research_mcp import server


def test_start_deep_research_returns_structured_only(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure start_deep_research returns clean CallToolResult without duplicate JSON in content."""
    monkeypatch.setattr(
        server,
        "_get_client_and_settings",
        lambda: (
            object(),
            server.Settings(api_key="x", model="m", deep_research_agent="agent", poll_interval_seconds=1.0),
        ),
    )
    monkeypatch.setattr(server, "sdk_start_deep_research", lambda _client, *, prompt, agent: {"id": "int_123", "status": "in_progress"})

    result = server.start_deep_research(prompt="Research Quantum Computing")
    assert isinstance(result, CallToolResult)
    assert result.content == []
    assert result.isError is False
    assert result.structuredContent is not None
    assert result.structuredContent["job_id"] == "int_123"
    assert result.structuredContent["status"] == "in_progress"


def test_start_deep_research_preserves_initial_status(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        server,
        "_get_client_and_settings",
        lambda: (
            object(),
            server.Settings(api_key="x", model="m", deep_research_agent="agent", poll_interval_seconds=1.0),
        ),
    )
    monkeypatch.setattr(
        server,
        "sdk_start_deep_research",
        lambda _client, *, prompt, agent: {"id": "int_456", "status": "failed"},
    )

    result = server.start_deep_research(prompt="Research Quantum Computing")
    assert result.structuredContent["status"] == "failed"


def test_check_deep_research_in_progress(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure check_deep_research reports in_progress status with uptime."""
    from datetime import datetime, timezone, timedelta

    created_time = datetime.now(timezone.utc) - timedelta(minutes=4, seconds=12)

    monkeypatch.setattr(
        server,
        "_get_client_and_settings",
        lambda: (
            object(),
            server.Settings(api_key="x", model="m", deep_research_agent="agent", poll_interval_seconds=1.0),
        ),
    )
    monkeypatch.setattr(
        server,
        "get_interaction",
        lambda _client, *, job_id: {"id": job_id, "status": "in_progress", "created": created_time},
    )

    result = server.check_deep_research(job_id="int_123")
    assert isinstance(result, CallToolResult)
    assert result.content == []
    assert result.isError is False
    assert result.structuredContent is not None
    assert result.structuredContent["job_id"] == "int_123"
    assert result.structuredContent["status"] == "in_progress"
    assert "4m" in result.structuredContent["uptime"]
    assert "report_text" not in result.structuredContent


def test_check_deep_research_failed_with_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure check_deep_research returns formatted failure error code and message."""
    monkeypatch.setattr(
        server,
        "_get_client_and_settings",
        lambda: (
            object(),
            server.Settings(api_key="x", model="m", deep_research_agent="agent", poll_interval_seconds=1.0),
        ),
    )
    monkeypatch.setattr(
        server,
        "get_interaction",
        lambda _client, *, job_id: {
            "id": job_id,
            "status": "failed",
            "error": {"code": "403", "message": "No sufficient credits for the request"},
        },
    )

    result = server.check_deep_research(job_id="int_123")
    assert isinstance(result, CallToolResult)
    assert result.structuredContent is not None
    assert result.structuredContent["job_id"] == "int_123"
    assert result.structuredContent["status"] == "failed"
    assert result.structuredContent["error"] == "Error 403 - No sufficient credits for the request"
    assert "report_text" not in result.structuredContent


def test_check_deep_research_completed(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure check_deep_research returns full report when completed."""
    monkeypatch.setattr(
        server,
        "_get_client_and_settings",
        lambda: (
            object(),
            server.Settings(api_key="x", model="m", deep_research_agent="agent", poll_interval_seconds=1.0),
        ),
    )
    monkeypatch.setattr(server, "get_interaction", lambda _client, *, job_id: {"id": job_id, "status": "completed"})
    monkeypatch.setattr(
        server,
        "interaction_to_result",
        lambda _interaction, *, include_citations=True: {
            "status": "completed",
            "text": "# Deep Research Findings\n\nQuantum advantage demonstrated.",
        },
    )

    result = server.check_deep_research(job_id="int_123", include_citations=True)
    assert isinstance(result, CallToolResult)
    assert result.content == []
    assert result.isError is False
    assert result.structuredContent is not None
    assert result.structuredContent["job_id"] == "int_123"
    assert result.structuredContent["status"] == "completed"
    assert "# Deep Research Findings" in result.structuredContent["report_text"]


def test_async_tools_fastmcp_validation(monkeypatch: pytest.MonkeyPatch) -> None:
    """Exercises FastMCP tool run with convert_result=True for both async tools."""
    monkeypatch.setattr(
        server,
        "_get_client_and_settings",
        lambda: (
            object(),
            server.Settings(api_key="x", model="m", deep_research_agent="agent", poll_interval_seconds=1.0),
        ),
    )
    monkeypatch.setattr(server, "sdk_start_deep_research", lambda _client, *, prompt, agent: {"id": "int_abc", "status": "in_progress"})
    monkeypatch.setattr(server, "get_interaction", lambda _client, *, job_id: {"id": job_id, "status": "completed"})
    monkeypatch.setattr(
        server,
        "interaction_to_result",
        lambda _interaction, *, include_citations=True: {
            "status": "completed",
            "text": "DONE REPORT",
        },
    )

    start_tool = Tool.from_function(server.start_deep_research, structured_output=True)
    check_tool = Tool.from_function(server.check_deep_research, structured_output=True)

    start_res = asyncio.run(start_tool.run({"prompt": "AI advancements"}, convert_result=True))
    assert isinstance(start_res, CallToolResult)
    assert start_res.structuredContent["job_id"] == "int_abc"

    check_res = asyncio.run(check_tool.run({"job_id": "int_abc", "include_citations": True}, convert_result=True))
    assert isinstance(check_res, CallToolResult)
    assert check_res.structuredContent["report_text"] == "DONE REPORT"
