import os
from typing import Literal

from deepagents import create_deep_agent  # pyright: ignore[reportMissingImports]
from deepagents.backends import FilesystemBackend
from tavily import TavilyClient  # pyright: ignore[reportMissingImports]

tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])


def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
):
    """Run a web search and return results."""
    return tavily_client.search(
        query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )


research_instructions = """Du er en ekspert-researcher.
Din opgave er at udføre grundig research og derefter skrive en grundig rapport.
Brug internet_search til at indsamle information.
Skriv dine fund til filer undervejs for at undgå at miste kontekst.
Brug write_todos til at planlægge dine research-skridt, før du starter.
Du skal svare på dansk.
"""

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",  # default model
    tools=[internet_search],
    system_prompt=research_instructions,
    backend=FilesystemBackend(root_dir=".", virtual_mode=True),
)
final_message = None
for chunk in agent.stream(
    {
        "messages": [
            {
                "role": "user",
                "content": "Undersøg hvordan AI anvendes i den offentlige sektor i Danmark, hvad er strategien og hvilke initiativer er i gang.",
            }
        ]
    },
    stream_mode="updates",
):
    for node, update in chunk.items():
        print(f"\n--- {node} ---")
        if not update:
            continue
        messages = update.get("messages", [])
        if hasattr(messages, "__iter__") and not isinstance(messages, str):
            msgs = list(messages)
        else:
            msgs = [messages] if messages else []
        for msg in msgs:
            if hasattr(msg, "content") and msg.content:
                print(msg.content)
                final_message = msg
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                for tc in msg.tool_calls:
                    print(f"[tool call] {tc['name']}({tc['args']})")

if final_message and hasattr(final_message, "content"):
    content = final_message.content
    if isinstance(content, list):
        content = "\n".join(
            block.get("text", "") if isinstance(block, dict) else str(block)
            for block in content
        )
    with open("rapport.md", "w", encoding="utf-8") as f:
        f.write(content)
    print("\nRapport gemt i rapport.md")
