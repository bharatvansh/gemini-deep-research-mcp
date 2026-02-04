# Gemini Deep Research MCP

[![PyPI version](https://img.shields.io/pypi/v/gemini-deep-research-mcp)](https://pypi.org/project/gemini-deep-research-mcp/)
[![npm version](https://img.shields.io/npm/v/@bharatvansh/gemini-deep-research-mcp)](https://www.npmjs.com/package/@bharatvansh/gemini-deep-research-mcp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An MCP server that exposes Gemini's **Deep Research Agent** for comprehensive web research.

## One-Click Install

| IDE | Install |
|-----|---------|
| **Cursor** | [![Install in Cursor](https://img.shields.io/badge/Install-Cursor-blue?logo=cursor)](https://cursor.com/en/install-mcp?name=gemini-deep-research&config=eyJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyJnZW1pbmktZGVlcC1yZXNlYXJjaC1tY3AiXSwiZW52Ijp7IkdFTUlOSV9BUElfS0VZIjoieW91ci1hcGkta2V5In19) |
| **VS Code** | [![Install in VS Code](https://img.shields.io/badge/Install-VS%20Code-007ACC?logo=visualstudiocode)](https://insiders.vscode.dev/redirect/mcp/install?name=gemini-deep-research&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22gemini-deep-research-mcp%22%5D%2C%22env%22%3A%7B%22GEMINI_API_KEY%22%3A%22your-api-key%22%7D%7D) |
| **VS Code Insiders** | [![Install in VS Code Insiders](https://img.shields.io/badge/Install-VS%20Code%20Insiders-24bfa5?logo=visualstudiocode)](https://insiders.vscode.dev/redirect/mcp/install?name=gemini-deep-research&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22gemini-deep-research-mcp%22%5D%2C%22env%22%3A%7B%22GEMINI_API_KEY%22%3A%22your-api-key%22%7D%7D&quality=insiders) |

> **Note:** After clicking, replace `your-api-key` with your [Gemini API key](https://aistudio.google.com/apikey). VS Code requires version 1.101+.

---

## Installation Methods

### Using npx (Node.js)

Requires [Node.js](https://nodejs.org/) 16+ and [uv](https://docs.astral.sh/uv/).

```bash
npx @bharatvansh/gemini-deep-research-mcp
```

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

<details>
<summary><strong>Windsurf config</strong></summary>

Add to `~/.codeium/windsurf/mcp_config.json` (macOS/Linux) or `%USERPROFILE%\.codeium\windsurf\mcp_config.json` (Windows):

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

<details>
<summary><strong>Cline config</strong></summary>

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

<details>
<summary><strong>Claude Code config</strong></summary>

Add to `~/.claude/settings.json`:

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

<details>
<summary><strong>Codex config</strong></summary>

Add to `~/.codex/config.toml`:

```toml
[mcp_servers.gemini-deep-research]
command = "uvx"
args = ["gemini-deep-research-mcp"]

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
<summary><strong>Antigravity config</strong></summary>

Add to your Antigravity `mcp_config.json`:

```json
{
  "gemini-deep-research": {
    "command": "uvx",
    "args": ["gemini-deep-research-mcp"],
    "env": {
      "GEMINI_API_KEY": "your-api-key"
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

<details>
<summary><strong>Windsurf config</strong></summary>

Add to `~/.codeium/windsurf/mcp_config.json` (macOS/Linux) or `%USERPROFILE%\.codeium\windsurf\mcp_config.json` (Windows):

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

<details>
<summary><strong>Cline config</strong></summary>

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

<details>
<summary><strong>Claude Code config</strong></summary>

Add to `~/.claude/settings.json`:

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

<details>
<summary><strong>Codex config</strong></summary>

Add to `~/.codex/config.toml`:

```toml
[mcp_servers.gemini-deep-research]
command = "gemini-deep-research-mcp"

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
<summary><strong>Antigravity config</strong></summary>

Add to your Antigravity `mcp_config.json`:

```json
{
  "gemini-deep-research": {
    "command": "gemini-deep-research-mcp",
    "env": {
      "GEMINI_API_KEY": "your-api-key"
    }
  }
}
```
</details>

---

### Antigravity

1. Open the **Agent side panel** → click **...** → **MCP Store**
2. Search for your MCP server or click **Add Custom Server**
3. Add this configuration to your `mcp_config.json`:

```json
{
  "gemini-deep-research": {
    "command": "uvx",
    "args": ["gemini-deep-research-mcp"],
    "env": {
      "GEMINI_API_KEY": "your-api-key"
    }
  }
}
```

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
