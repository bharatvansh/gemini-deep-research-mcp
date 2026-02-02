# Gemini Deep Research MCP

[![PyPI version](https://img.shields.io/pypi/v/gemini-deep-research-mcp)](https://pypi.org/project/gemini-deep-research-mcp/)
[![npm version](https://img.shields.io/npm/v/gemini-deep-research-mcp)](https://www.npmjs.com/package/gemini-deep-research-mcp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An MCP server that exposes Gemini's **Deep Research Agent** for comprehensive web research.

## One-Click Install

### Cursor

[![Install MCP Server](https://cursor.com/deeplink/mcp-install-dark.svg)](https://cursor.com/install-mcp?name=gemini-deep-research&config=eyJjb21tYW5kIjogInV2eCIsICJhcmdzIjogWyJnZW1pbmktZGVlcC1yZXNlYXJjaC1tY3AiXSwgImVudiI6IHsiR0VNSU5JX0FQSV9LRVkiOiAieW91ci1hcGkta2V5In19)

Click the button, then replace `your-api-key` with your [Gemini API key](https://aistudio.google.com/apikey).

---

## Installation Methods

### Using npx (Node.js)

Requires [Node.js](https://nodejs.org/) 16+ and [uv](https://docs.astral.sh/uv/).

```bash
npx gemini-deep-research-mcp
```

<details>
<summary><strong>VS Code config</strong></summary>

```json
{
  "servers": {
    "gemini-deep-research": {
      "command": "npx",
      "args": ["-y", "gemini-deep-research-mcp"],
      "env": {
        "GEMINI_API_KEY": "your-api-key"
      }
    }
  }
}
```
</details>

<details>
<summary><strong>Claude Desktop config</strong></summary>

```json
{
  "mcpServers": {
    "gemini-deep-research": {
      "command": "npx",
      "args": ["-y", "gemini-deep-research-mcp"],
      "env": {
        "GEMINI_API_KEY": "your-api-key"
      }
    }
  }
}
```
</details>

---

### Using uvx (Python)

Requires [uv](https://docs.astral.sh/uv/).

```bash
uvx gemini-deep-research-mcp
```

<details>
<summary><strong>VS Code config</strong></summary>

```json
{
  "servers": {
    "gemini-deep-research": {
      "command": "uvx",
      "args": ["gemini-deep-research-mcp"],
      "env": {
        "GEMINI_API_KEY": "your-api-key"
      }
    }
  }
}
```
</details>

<details>
<summary><strong>Claude Desktop config</strong></summary>

```json
{
  "mcpServers": {
    "gemini-deep-research": {
      "command": "uvx",
      "args": ["gemini-deep-research-mcp"],
      "env": {
        "GEMINI_API_KEY": "your-api-key"
      }
    }
  }
}
```
</details>

---

### Using pip

```bash
pip install gemini-deep-research-mcp
```

<details>
<summary><strong>VS Code config</strong></summary>

```json
{
  "servers": {
    "gemini-deep-research": {
      "command": "gemini-deep-research-mcp",
      "env": {
        "GEMINI_API_KEY": "your-api-key"
      }
    }
  }
}
```
</details>

<details>
<summary><strong>Claude Desktop config</strong></summary>

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
</details>

---

## Prerequisites

<details>
<summary><strong>Install uv (required for npx/uvx methods)</strong></summary>

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
</details>

---

## Tool: `gemini_deep_research`

Conducts comprehensive web research using Gemini's Deep Research Agent. Blocks until research completes (typically 10-20 minutes).

**When to use:**
- Complex topics requiring multi-source analysis
- Synthesized information from the web
- Fact-checking and cross-referencing

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | ✓ | — | Your research question or topic |
| `include_citations` | boolean | | `true` | Include resolved source URLs |

| Output | Description |
|--------|-------------|
| `status` | `completed`, `failed`, or `cancelled` |
| `report_text` | Synthesized research report |

## Configuration

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GEMINI_API_KEY` | ✓ | — | Your [Gemini API key](https://aistudio.google.com/apikey) |
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
