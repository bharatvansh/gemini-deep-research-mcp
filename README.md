# Gemini Deep Research MCP

An MCP server that exposes Gemini's **Deep Research Agent** for comprehensive web research.

## Quick Start

```bash
pip install gemini-deep-research-mcp
```

Set your API key:
```bash
export GEMINI_API_KEY="your-api-key"  # macOS/Linux
set GEMINI_API_KEY=your-api-key       # Windows CMD
$env:GEMINI_API_KEY="your-api-key"    # Windows PowerShell
```

## MCP Client Setup

### VS Code (Copilot)

Add to your VS Code settings or `.vscode/mcp.json`:

```json
{
  "mcp": {
    "servers": {
      "gemini-deep-research": {
        "command": "gemini-deep-research-mcp",
        "env": {
          "GEMINI_API_KEY": "your-api-key"
        }
      }
    }
  }
}
```

### Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "gemini-deep-research": {
      "command": "gemini-deep-research-mcp",
      "env": {
        "GEMINI_API_KEY": "your-api-key"
      }
    }
  }
}
```

> **Windows**: If `gemini-deep-research-mcp` isn't in PATH, use full path: `C:\\Users\\YOU\\...\\python.exe` with args `["-m", "gemini_deep_research_mcp"]`

## Tool: `gemini_deep_research`

Conducts comprehensive web research using Gemini's Deep Research Agent. Blocks until research completes (typically 10-20 minutes).

**When to use:**
- Complex topics requiring multi-source analysis
- Synthesized information from the web
- Fact-checking and cross-referencing

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | ✓ | — | Your research question or topic |
| `include_citations` | boolean | | `true` | Include resolved source URLs |

**Output:**

| Field | Description |
|-------|-------------|
| `status` | `completed`, `failed`, or `cancelled` |
| `report_text` | Synthesized research report |

## Configuration

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GEMINI_API_KEY` | ✓ | — | Your Gemini API key |
| `GEMINI_DEEP_RESEARCH_AGENT` | | `deep-research-pro-preview-12-2025` | Model to use |

## Development

```bash
git clone https://github.com/bharatvansh/gemini-deep-research-mcp.git
cd gemini-deep-research-mcp
pip install -e .[dev]
pytest
```

## License

MIT
