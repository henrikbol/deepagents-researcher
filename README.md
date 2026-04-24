# DeepAgents Showcase

A minimal example of [deepagents](https://pypi.org/project/deepagents/) — LangChain's general-purpose agent framework built on LangGraph with built-in planning, file I/O, sub-agent spawning, and tool calling.

## What it does

`researcher.py` runs a Danish-language research agent that:

1. Plans its research steps using a todo list (`write_todos`)
2. Searches the web via [Tavily](https://tavily.com/)
3. Writes intermediate findings to files to preserve context across long runs
4. Produces a final report saved to `rapport.md`

The current task: *AI i den offentlige sektor i Danmark* — strategy, initiatives, and current state.

## Setup

Requires Python 3.13+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

Copy `.env.example` to `.env` and fill in your keys:

```bash
cp .env.example .env
```

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | For `--model claude` | [console.anthropic.com](https://console.anthropic.com/) |
| `GOOGLE_API_KEY` | For `--model gemma` | [aistudio.google.com](https://aistudio.google.com/) → API Keys |
| `TAVILY_API_KEY` | Yes | [app.tavily.com](https://app.tavily.com/) |
| `LANGSMITH_TRACING` | No | Set to `true` to enable LangSmith tracing |
| `LANGSMITH_API_KEY` | No | Required if `LANGSMITH_TRACING=true` |

The project uses [direnv](https://direnv.net/) via `.envrc` — run `direnv allow` once to auto-load the `.env` file when entering the directory.

## Run

```bash
# Default: Claude Sonnet (Anthropic)
uv run python researcher.py

# Google Gemma 3 4B via Google AI Studio
uv run python researcher.py --model gemma
```

The agent streams its progress to the terminal and saves the final report to `rapport.md`.

## Models

| Flag | Model | Provider |
|------|-------|----------|
| `--model claude` (default) | `claude-sonnet-4-6` | Anthropic — best tool calling reliability |
| `--model gemma` | `gemma-4-26b-a4b-it` | Google AI Studio — Gemma 4 MoE with 4B active params |

> **Note:** Gemma via Google AI Studio supports tool calling, but may be less reliable than Claude for complex multi-step agent runs.

## Key configuration

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `--model` | `claude` / `gemma` | Switch LLM at runtime |
| `backend` | `FilesystemBackend(root_dir=".", virtual_mode=True)` | Writes files to the project directory |
| `tools` | `internet_search` (Tavily) | Web search capability |
| `stream_mode` | `"updates"` | Print each agent step as it happens |

## Dependencies

- [deepagents](https://pypi.org/project/deepagents/) — agent framework by LangChain
- [tavily-python](https://pypi.org/project/tavily-python/) — web search API
- [langchain-google-genai](https://pypi.org/project/langchain-google-genai/) — Google AI Studio / Gemma support
