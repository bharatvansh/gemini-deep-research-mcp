from datetime import datetime, timezone
import logging
import sys
from typing import Annotated, Any, Optional, TypedDict

from mcp.server.fastmcp import FastMCP
from mcp.types import CallToolResult, ToolAnnotations

from .config import Settings, load_settings
from .extract import interaction_to_result
from .gemini import create_client, get_interaction, start_deep_research as sdk_start_deep_research


logger = logging.getLogger(__name__)


class StartResearchOutput(TypedDict):
    job_id: str
    status: str


class CheckResearchOutput(TypedDict, total=False):
    job_id: str
    status: str
    report_text: str
    uptime: str
    error: str


def _configure_logging() -> None:
    # IMPORTANT: stdout is reserved for MCP protocol.
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
        stream=sys.stderr,
    )


_configure_logging()


mcp = FastMCP("Gemini Deep Research MCP")


def _get_client_and_settings() -> tuple[Any, Settings]:
    settings = load_settings()
    client = create_client(settings)
    return client, settings


def _require_nonempty(value: Optional[str], *, field: str) -> str:
    if value is None:
        raise ValueError(f"`{field}` is required")
    value = str(value)
    if not value.strip():
        raise ValueError(f"`{field}` is required")
    return value.strip()


def _format_uptime(created: Any) -> Optional[str]:
    if not created:
        return None
    try:
        if isinstance(created, str):
            created_dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
        elif isinstance(created, datetime):
            created_dt = created
        elif isinstance(created, (int, float)):
            created_dt = datetime.fromtimestamp(created, tz=timezone.utc)
        else:
            return None

        if created_dt.tzinfo is None:
            created_dt = created_dt.replace(tzinfo=timezone.utc)

        now = datetime.now(timezone.utc)
        diff_seconds = max(0, int((now - created_dt).total_seconds()))

        hours = diff_seconds // 3600
        mins = (diff_seconds % 3600) // 60
        secs = diff_seconds % 60

        if hours > 0:
            return f"{hours}h {mins}m {secs}s"
        elif mins > 0:
            return f"{mins}m {secs}s"
        else:
            return f"{secs}s"
    except Exception:
        return None


def _format_error_detail(interaction: Any) -> Optional[str]:
    error = getattr(interaction, "error", None) or (
        interaction.get("error") if isinstance(interaction, dict) else None
    )
    if not error:
        return None
    code = getattr(error, "code", None) or (error.get("code") if isinstance(error, dict) else None)
    message = getattr(error, "message", None) or (error.get("message") if isinstance(error, dict) else None)
    if code and message:
        return f"Error {code} - {message}"
    if message:
        return str(message)
    if code:
        return f"Error {code}"
    return None


_START_DEEP_RESEARCH_DESCRIPTION = """
Initiates a deep, multi-step web research job in the background using Google's Deep Research Agent. Returns a job_id, which you can use to check the status of completion using check_deep_research(job_id=...).

Parameters:
- `prompt`: The comprehensive research question or topic to investigate (required)

Returns:
- `job_id`: Unique tracking ID for the research job
- `status`: Initial job state (typically 'in_progress')
""".strip()


_CHECK_DEEP_RESEARCH_DESCRIPTION = """
Checks the status of a Deep Research job using its job_id and returns the complete report once finished.

Parameters:
- `job_id`: The tracking ID returned by `start_deep_research` (required)
- `include_citations`: Whether to include source URLs in the report (default: true)

Returns:
- `job_id`: The tracking ID of the research job
- `status`: Current job state ('in_progress', 'completed', 'failed', or 'cancelled')
- `report_text`: The synthesized research report when completed
- `uptime`: Elapsed time while the job is in progress, when available
- `error`: Failure details, when the API provides them
""".strip()


@mcp.tool(
    name="start_deep_research",
    title="Start Gemini Deep Research",
    description=_START_DEEP_RESEARCH_DESCRIPTION,
    annotations=ToolAnnotations(
        openWorldHint=True,
        readOnlyHint=False,
        idempotentHint=False,
    ),
    structured_output=True,
)
def start_deep_research(
    prompt: str,
) -> Annotated[CallToolResult, StartResearchOutput]:
    """Initiate a deep research job and immediately return tracking ID."""
    prompt_clean = _require_nonempty(prompt, field="prompt")

    client, settings = _get_client_and_settings()

    initial = sdk_start_deep_research(client, prompt=prompt_clean, agent=settings.deep_research_agent)
    job_id = getattr(initial, "id", None) or (
        initial.get("id") if isinstance(initial, dict) else None
    )
    if not job_id:
        raise RuntimeError("Gemini SDK did not return a research job id.")

    status = getattr(initial, "status", None) or (
        initial.get("status") if isinstance(initial, dict) else None
    ) or "in_progress"

    payload: StartResearchOutput = {"job_id": str(job_id), "status": str(status)}

    return CallToolResult(content=[], structuredContent=payload, isError=False)


@mcp.tool(
    name="check_deep_research",
    title="Check Gemini Deep Research",
    description=_CHECK_DEEP_RESEARCH_DESCRIPTION,
    annotations=ToolAnnotations(
        openWorldHint=True,
        readOnlyHint=True,
        idempotentHint=True,
    ),
    structured_output=True,
)
def check_deep_research(
    job_id: str,
    include_citations: bool = True,
) -> Annotated[CallToolResult, CheckResearchOutput]:
    """Check the status of a deep research job and return the report if ready."""
    job_id_clean = _require_nonempty(job_id, field="job_id")

    client, _settings = _get_client_and_settings()

    interaction = get_interaction(client, job_id=job_id_clean)
    if interaction is None:
        raise ValueError(f"No research job found for ID: {job_id_clean}")

    status = getattr(interaction, "status", None) or (
        interaction.get("status") if isinstance(interaction, dict) else None
    ) or "unknown"
    status_str = str(status)

    created = getattr(interaction, "created", None) or (
        interaction.get("created") if isinstance(interaction, dict) else None
    )

    if status_str == "completed":
        result = interaction_to_result(interaction, include_citations=include_citations)
        payload: CheckResearchOutput = {
            "job_id": job_id_clean,
            "status": "completed",
            "report_text": result.get("text", ""),
        }
    elif status_str == "in_progress":
        uptime = _format_uptime(created)
        payload = {
            "job_id": job_id_clean,
            "status": status_str,
        }
        if uptime:
            payload["uptime"] = uptime
    elif status_str in {"failed", "cancelled"}:
        err_detail = _format_error_detail(interaction)
        payload = {
            "job_id": job_id_clean,
            "status": status_str,
        }
        if err_detail:
            payload["error"] = err_detail
    else:
        result = interaction_to_result(interaction, include_citations=include_citations)
        report_text = result.get("text", "")
        payload = {
            "job_id": job_id_clean,
            "status": status_str,
        }
        if report_text:
            payload["report_text"] = report_text

    return CallToolResult(content=[], structuredContent=payload, isError=False)


def main() -> None:
    # Run over STDIO.
    logger.info("Starting Gemini Deep Research MCP server (stdio)")
    mcp.run()
