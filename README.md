# Gemini Deep Research MCP (Python)

An MCP server (STDIO / JSON-RPC) that exposes two tools backed by the Gemini **Interactions API**:

- `gemini_deep_research` — start a Deep Research job or poll an existing one
- `gemini_deep_research_followup` — ask a follow-up question using a prior interaction as context

This uses:

- Python `mcp` SDK (`FastMCP`)
- Official `google-genai` SDK (`from google import genai`)

## Tools

### `gemini_deep_research`

Starts a Deep Research task using the specialized **Gemini Deep Research Agent** (default: `deep-research-pro-preview-12-2025`) or resumes polling an existing `interaction_id`.

You must provide **exactly one** of:

- `prompt` (start mode)
- `interaction_id` (poll mode)

Inputs:

- `prompt` (string): required when starting new research
- `interaction_id` (string): required when polling/resuming an existing interaction
- `wait` (boolean, default `true`): poll until completion or timeout
- `timeout_seconds` (number, default `600`): must be > 0 when `wait=true`

Outputs:

- `interaction_id`
- `status`: raw Gemini interaction status string (terminal statuses are usually `completed`, `failed`, or `cancelled`)
- `report_text`: best-effort concatenated text from `Interaction.outputs`
- `citations`: extracted citation-like annotations if present

### `gemini_deep_research_followup`

Asks a follow-up question using a prior research interaction as context, powered by **Gemini 3** models.

Inputs:

- `previous_interaction_id` (string): required
- `question` (string): required
- `model` (string, optional): The model ID to use (e.g., `gemini-3-pro-preview` or `gemini-3-flash-preview`). Defaults to the configured `GEMINI_MODEL`.

Outputs:

- `interaction_id`
- `answer_text`
- `citations`

## Configuration

Environment variables (loaded from `.env` if present):

- `GEMINI_API_KEY` (required) — falls back to `GOOGLE_API_KEY` if set
- `GEMINI_MODEL` (default `gemini-3-pro-preview`)
- `GEMINI_DEEP_RESEARCH_AGENT` (default `deep-research-pro-preview-12-2025`)

Notes:

- For Deep Research, the Interactions API requires `background=True` **and** `store=True`.
- Logs are written to **stderr** (stdout is reserved for MCP protocol).

## VS Code MCP setup

This repo includes a starter `.vscode/mcp.json`.

Typical flow:

1. Create / activate a venv and install the package (`pip install -e .`).
2. Set `GEMINI_API_KEY` in your environment (or edit `.env`).
3. Reload VS Code so MCP picks up the server.

## Claude Desktop (Windows) setup

Claude Desktop uses a config file (usually `claude_desktop_config.json`) with an `mcpServers` map.

On Windows, **escape backslashes** in JSON, and prefer absolute paths.

Example (adjust Python path / venv path to your machine):

```json
{
  "mcpServers": {
    "gemini-deep-research": {
      "command": "C:\\Path\\To\\python.exe",
      "args": ["-m", "gemini_deep_research_mcp"],
      "env": {
        "GEMINI_API_KEY": "YOUR_KEY_HERE"
      }
    }
  }
}
```

## Development

- Package code is under `src/gemini_deep_research_mcp/`.
- Tests live in `tests/`.
