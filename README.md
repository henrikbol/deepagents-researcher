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
| `ANTHROPIC_API_KEY` | Yes | [console.anthropic.com](https://console.anthropic.com/) |
| `TAVILY_API_KEY` | Yes | [app.tavily.com](https://app.tavily.com/) |
| `LANGSMITH_TRACING` | No | Set to `true` to enable LangSmith tracing |
| `LANGSMITH_API_KEY` | No | Required if `LANGSMITH_TRACING=true` |

The project uses [direnv](https://direnv.net/) via `.envrc` — run `direnv allow` once to auto-load the `.env` file when entering the directory.

## Run

```bash
uv run python researcher.py
```

The agent streams its progress to the terminal and saves the final report to `rapport.md`.

## Key configuration

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `model` | `anthropic:claude-sonnet-4-6` | The LLM powering the agent |
| `backend` | `FilesystemBackend(root_dir=".", virtual_mode=True)` | Writes files to the project directory |
| `tools` | `internet_search` (Tavily) | Web search capability |
| `stream_mode` | `"updates"` | Print each agent step as it happens |

## Dependencies

- [deepagents](https://pypi.org/project/deepagents/) — agent framework by LangChain
- [tavily-python](https://pypi.org/project/tavily-python/) — web search API
