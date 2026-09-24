"""
CLI entry point for the Memory / RAG Agent.

Usage (run from the repository root so the ``projects`` package resolves):
    python -m projects.ai_agents.agent4_memory_rag.main "What is projects/ai_agents?"
    python -m projects.ai_agents.agent4_memory_rag.main remember "Some new fact to store"
"""

import os
import sys

from dotenv import load_dotenv

from projects.utils.logging_config import setup_logger

from .agent import MemoryAgent
from .memory_store import MemoryStore

DEFAULT_MEMORY_PATH = os.path.join(os.path.dirname(__file__), "memory_store.json")


def main() -> None:
    """Dispatch to `remember` or `ask` based on the first CLI argument."""
    load_dotenv()
    setup_logger(__name__, level="INFO")

    args = sys.argv[1:] or ["ask", "What is projects/ai_agents?"]
    command = args[0] if args[0] in ("remember", "ask") else "ask"
    text = " ".join(args[1:] if args[0] == command else args)

    memory_path = os.getenv("AI_AGENTS_MEMORY_PATH", DEFAULT_MEMORY_PATH)
    store = MemoryStore(path=memory_path)
    agent = MemoryAgent(store=store)

    if command == "remember":
        doc_id = agent.remember(text)
        print(f"Stored as document '{doc_id}' in {memory_path}")
    else:
        print(f"Q: {text}\n")
        print(agent.ask(text))


if __name__ == "__main__":
    main()
