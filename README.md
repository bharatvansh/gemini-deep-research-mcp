# Gemini Deep Research MCP (Python)

An MCP server (STDIO / JSON-RPC) that exposes a tool backed by the Gemini **Interactions API**:

- `gemini_deep_research` — conduct comprehensive web research using Gemini's Deep Research Agent

This uses:

- Python `mcp` SDK (`FastMCP`)
- Official `google-genai` SDK (`from google import genai`)

## Tools

### `gemini_deep_research`

Conducts comprehensive web research using Gemini's Deep Research Agent (default: `deep-research-pro-preview-12-2025`). The tool blocks until research completes, typically taking 10-20 minutes.

**When to use:**

- Researching complex topics requiring multi-source analysis
- Need synthesized information from the web
- Require fact-checking and cross-referencing of information

**Inputs:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | ✓ | — | Your research question or topic |
| `timeout_seconds` | number | | 900 | Max time to wait for completion (must be > 0) |

**Outputs:**

| Field | Description |
|-------|-------------|
| `status` | Final state: `completed`, `failed`, or `cancelled` |
| `report_text` | The synthesized research report with findings |

## Configuration

Environment variables (loaded from `.env` if present):

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GEMINI_API_KEY` | ✓ | — | Your Gemini API key (falls back to `GOOGLE_API_KEY` if set) |
| `GEMINI_DEEP_RESEARCH_AGENT` | | `deep-research-pro-preview-12-2025` | Deep Research agent model |

**Notes:**

- For Deep Research, the Interactions API requires `background=True` **and** `store=True`.
- Logs are written to **stderr** (stdout is reserved for MCP protocol).

## Installation

```bash
# Clone the repository
git clone https://github.com/your-username/gemini-deep-research-mcp.git
cd gemini-deep-research-mcp

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate    # Windows
# source .venv/bin/activate  # macOS/Linux

# Install the package
pip install -e .
```

## VS Code MCP Setup

This repo includes a starter `.vscode/mcp.json`.

1. Create / activate a venv and install the package (`pip install -e .`).
2. Set `GEMINI_API_KEY` in your environment (or edit `.env`).
3. Reload VS Code so MCP picks up the server.

## Claude Desktop (Windows) Setup

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

Run tests:

```bash
pip install -e .[dev]
pytest
```

## License

MIT
