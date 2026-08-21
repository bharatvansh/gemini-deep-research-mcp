# Gemini Deep Research MCP

[![npm version](https://img.shields.io/npm/v/@bharatvansh/gemini-deep-research-mcp)](https://www.npmjs.com/package/@bharatvansh/gemini-deep-research-mcp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An MCP server that exposes Gemini's **Deep Research Agent** for comprehensive web research.

## Quick Start

```bash
npx @bharatvansh/gemini-deep-research-mcp
```

> **Requires:** [Node.js](https://nodejs.org/) 16+ and [uv](https://docs.astral.sh/uv/)

## One-Click Install

| IDE | Install |
|-----|---------|
| **Cursor** | [![Install in Cursor](https://img.shields.io/badge/Install-Cursor-blue?logo=cursor)](https://cursor.com/en/install-mcp?name=gemini-deep-research&config=eyJjb21tYW5kIjoibnB4IiwiYXJncyI6WyIteSIsIkBiaGFyYXR2YW5zaC9nZW1pbmktZGVlcC1yZXNlYXJjaC1tY3AiXSwiZW52Ijp7IkdFTUlOSV9BUElfS0VZIjoieW91ci1hcGkta2V5In19) |
| **VS Code** | [![Install in VS Code](https://img.shields.io/badge/Install-VS%20Code-007ACC?logo=visualstudiocode)](https://insiders.vscode.dev/redirect/mcp/install?name=gemini-deep-research&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40bharatvansh%2Fgemini-deep-research-mcp%22%5D%2C%22env%22%3A%7B%22GEMINI_API_KEY%22%3A%22your-api-key%22%7D%7D) |
| **VS Code Insiders** | [![Install in VS Code Insiders](https://img.shields.io/badge/Install-VS%20Code%20Insiders-24bfa5?logo=visualstudiocode)](https://insiders.vscode.dev/redirect/mcp/install?name=gemini-deep-research&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40bharatvansh%2Fgemini-deep-research-mcp%22%5D%2C%22env%22%3A%7B%22GEMINI_API_KEY%22%3A%22your-api-key%22%7D%7D&quality=insiders) |

> **Note:** After clicking, replace `your-api-key` with your [Gemini API key](https://aistudio.google.com/apikey). VS Code requires version 1.101+.

---

## Configuration

<details>
<summary><strong>VS Code config</strong></summary>

```json
{
  "servers": {
    "gemini-deep-research": {
      "command": "npx",
      "args": ["-y", "@bharatvansh/gemini-deep-research-mcp"],
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
      "args": ["-y", "@bharatvansh/gemini-deep-research-mcp"],
      "env": {
        "GEMINI_API_KEY": "your-api-key"
      }
    }
  }
}
```
</details>

<details>
<summary><strong>Windsurf config</strong></summary>

Add to `~/.codeium/windsurf/mcp_config.json` (macOS/Linux) or `%USERPROFILE%\.codeium\windsurf\mcp_config.json` (Windows):

```json
{
  "mcpServers": {
    "gemini-deep-research": {
      "command": "npx",
      "args": ["-y", "@bharatvansh/gemini-deep-research-mcp"],
      "env": {
        "GEMINI_API_KEY": "your-api-key"
      }
    }
  }
}
```
</details>

<details>
<summary><strong>Cline config</strong></summary>

```json
{
  "mcpServers": {
    "gemini-deep-research": {
      "command": "npx",
      "args": ["-y", "@bharatvansh/gemini-deep-research-mcp"],
      "env": {
        "GEMINI_API_KEY": "your-api-key"
      }
    }
  }
}
```
</details>

<details>
<summary><strong>Claude Code config</strong></summary>

Add to `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "gemini-deep-research": {
      "command": "npx",
      "args": ["-y", "@bharatvansh/gemini-deep-research-mcp"],
      "env": {
        "GEMINI_API_KEY": "your-api-key"
      }
    }
  }
}
```
</details>

<details>
<summary><strong>Codex config</strong></summary>

Add to `~/.codex/config.toml`:

```toml
[mcp_servers.gemini-deep-research]
command = "npx"
args = ["-y", "@bharatvansh/gemini-deep-research-mcp"]

[mcp_servers.gemini-deep-research.env]
GEMINI_API_KEY = "your-api-key"
```
</details>

<details>
<summary><strong>Cursor config</strong></summary>

Add to `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "gemini-deep-research": {
      "command": "npx",
      "args": ["-y", "@bharatvansh/gemini-deep-research-mcp"],
      "env": {
        "GEMINI_API_KEY": "your-api-key"
      }
    }
  }
}
```
</details>

<details>
<summary><strong>Antigravity config</strong></summary>

Add to your Antigravity `mcp_config.json`:

```json
{
  "gemini-deep-research": {
    "command": "npx",
    "args": ["-y", "@bharatvansh/gemini-deep-research-mcp"],
    "env": {
      "GEMINI_API_KEY": "your-api-key"
    }
  }
}
```
</details>

---

## Prerequisites

<details>
<summary><strong>Install uv (required)</strong></summary>

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
</details>

---

## Tools

### 1. `start_deep_research`

Initiates a deep, multi-step web research job in the background using Google's Deep Research Agent. Returns a `job_id`, which you can use to check the status of completion using `check_deep_research(job_id=...)`.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | ✓ | — | Your comprehensive research question or topic |

| Output | Description |
|--------|-------------|
| `job_id` | Unique tracking ID for the research job |
| `status` | Initial job state (e.g. `in_progress`) |

---

### 2. `check_deep_research`

Checks the status of a Deep Research job using its `job_id` and returns the complete report once finished.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `job_id` | string | ✓ | — | The research tracking ID from `start_deep_research` |
| `include_citations` | boolean | | `true` | Include source URLs in the report |

| Output | Description |
|--------|-------------|
| `job_id` | The tracking ID of the research job |
| `status` | Exact current job state (`in_progress`, `completed`, `failed`, or `cancelled`) |
| `report_text` | Synthesized markdown research report (when `completed`) |
| `uptime` | Elapsed time while the job is in progress, when available |
| `error` | Failure details, when the API provides them |

## Configuration

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GEMINI_API_KEY` | ✓ | — | Your [Gemini API key](https://aistudio.google.com/apikey) |
| `GEMINI_DEEP_RESEARCH_AGENT` | | `deep-research-preview-04-2026` | Deep Research agent to use. Set to `deep-research-max-preview-04-2026` for maximum thoroughness, or `deep-research-preview-04-2026` for standard speed. |
| `GEMINI_MODEL` | | `gemini-3.5-flash` | Default Gemini model fallback for other tasks. |

## Links

- 📦 [PyPI Package](https://pypi.org/project/gemini-deep-research-mcp/)
- 🔧 [GitHub Repository](https://github.com/bharatvansh/gemini-deep-research-mcp)
- 🔑 [Get Gemini API Key](https://aistudio.google.com/apikey)

## License

MIT
