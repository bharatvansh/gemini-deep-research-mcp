# Plan: Gemini Deep Research MCP

## Core Overview
This MCP server integrates the **Gemini Deep Research Agent** and **Gemini 3 models** into any MCP host (e.g., VS Code, Claude Desktop). It exposes specialized tools for long-running research tasks and stateful follow-up conversations.

## Architecture
- **Language**: Python (using `mcp` SDK + `FastMCP`)
- **API Client**: Official `google-genai` SDK
- **Transport**: STDIO (JSON-RPC)
- **API Surface**: Gemini Interactions API (exclusive for Deep Research)

## Tool Specifications

### 1. `gemini_deep_research`
Starts a new deep research task or resumes polling an existing one.
- **Inputs**:
  - `prompt` (string): Required for new research.
  - `interaction_id` (string): Optional. If provided, the tool polls/resumes the existing interaction.
  - `wait` (boolean, default: `true`): If true, polls until completion or timeout.
  - `timeout_seconds` (number, default: `600`): Max time to wait.
- **Outputs**:
  - `interaction_id`: Used to poll or ask follow-ups.
  - `status`: `in_progress`, `completed`, `failed`, or `cancelled`.
  - `report_text`: The final research report or latest findings.
  - `citations`: Extracted source metadata (annotations).

### 2. `gemini_deep_research_followup`
Asks a follow-up question regarding a completed (or in-progress) deep research interaction.
- **Inputs**:
  - `previous_interaction_id` (string): Required ID of the research interaction.
  - `question` (string): The follow-up query.
  - `model` (enum: `"flash"`, `"pro"`, default: `"pro"`): Which model to use for the response.
- **Outputs**:
  - `interaction_id`: New interaction ID for this turn.
  - `answer_text`: The model's response.
  - `citations`: Source metadata if provided.

## Configuration (Environment Variables)
- `GEMINI_API_KEY`: Required (supports `GOOGLE_API_KEY` fallback).
- `GEMINI_FLASH_MODEL`: (default: `gemini-3-flash-preview`)
- `GEMINI_PRO_MODEL`: (default: `gemini-3-pro-preview`)
- `GEMINI_DEEP_RESEARCH_AGENT`: (default: `deep-research-pro-preview-12-2025`)

## Implementation Roadmap

### Step 1: Initialization
- Scaffold project with `pyproject.toml` and `src/` layout.
- Configure logging to `stderr` (crucial for MCP STDIO).
- Setup `.env` and `.env.example` handling.

### Step 2: Gemini Client Wrapper
- Initialize `genai.Client`.
- Implement wrapper for `interactions.create` with `background=True` for agents.
- Implement polling logic for `interactions.get`.

### Step 3: MCP Tool Implementation
- Define `@mcp.tool` for Deep Research with logic to handle start vs. resume.
- Define `@mcp.tool` for Follow-up using `previous_interaction_id`.
- Extract text and annotations from `Interaction.outputs` into user-friendly strings/objects.

### Step 4: Client Integration & Verification
- Create `.vscode/mcp.json` for VS Code testing.
- Document paths and escaping for Claude Desktop (Windows).
- Verify tool discovery and functional workflow (Research -> Poll -> Follow-up).

## Key Constraints & Notes
- **Interactions API (Beta)**: Features may change; production stability uses `generateContent` (but not for research).
- **Background Execution**: Deep Research *requires* `background=True` and `store=True`.
- **Retention**: Free tier interactions usually expire in 1 day; paid tier in 55 days.
- **Model Compatibility**: Use Gemini 3 preview IDs as defaults.
