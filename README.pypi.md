# Gemini Deep Research MCP

[![PyPI version](https://img.shields.io/pypi/v/gemini-deep-research-mcp)](https://pypi.org/project/gemini-deep-research-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An MCP server that exposes Gemini's **Deep Research Agent** for comprehensive web research.

## Quick Start

```bash
# Recommended (zero-install)
uvx gemini-deep-research-mcp

# Or install globally
pip install gemini-deep-research-mcp
gemini-deep-research-mcp
```

## One-Click Install

| IDE | Install |
|-----|---------|
| **Cursor** | [![Install in Cursor](https://img.shields.io/badge/Install-Cursor-blue?logo=cursor)](https://cursor.com/install-mcp?name=gemini-deep-research&config=eyJjb21tYW5kIjogInV2eCIsICJhcmdzIjogWyJnZW1pbmktZGVlcC1yZXNlYXJjaC1tY3AiXSwgImVudiI6IHsiR0VNSU5JX0FQSV9LRVkiOiAieW91ci1hcGkta2V5In19) |
| **VS Code** | [![Install in VS Code](https://img.shields.io/badge/Install-VS%20Code-007ACC?logo=visualstudiocode)](vscode:mcp/install?config=%7B%22name%22%3A%20%22gemini-deep-research%22%2C%20%22command%22%3A%20%22uvx%22%2C%20%22args%22%3A%20%5B%22gemini-deep-research-mcp%22%5D%2C%20%22env%22%3A%20%7B%22GEMINI_API_KEY%22%3A%20%22your-api-key%22%7D%7D) |

> Replace `your-api-key` with your [Gemini API key](https://aistudio.google.com/apikey).

## Configuration

**VS Code** (`.vscode/mcp.json`):

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

**Claude Desktop** (`claude_desktop_config.json`):

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

## Tool

### `gemini_deep_research`

Performs comprehensive web research using Gemini's Deep Research Agent.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | ✅ | Research topic or question |
| `include_citations` | boolean | ❌ | Include source citations (default: true) |

## Links

- 📦 [npm Package](https://www.npmjs.com/package/@bharatvansh/gemini-deep-research-mcp)
- 🔧 [GitHub Repository](https://github.com/bharatvansh/gemini-deep-research-mcp)
- 🔑 [Get Gemini API Key](https://aistudio.google.com/apikey)

## License

MIT
