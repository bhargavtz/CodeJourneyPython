"""
CLI entry point for the Web Search Agent.

Usage (run from the repository root so the ``projects`` package resolves):
    python -m projects.ai_agents.agent1_web_search.main "your question here"
"""

import sys

from dotenv import load_dotenv

from projects.utils.logging_config import setup_logger

from .agent import WebSearchAgent


def main() -> None:
    """Answer the question passed on the command line."""
    load_dotenv()
    setup_logger(__name__, level="INFO")

    question = " ".join(sys.argv[1:]) or "What is the most recent stable Python release?"
    print(f"Q: {question}\n")

    agent = WebSearchAgent()
    print(agent.ask(question))


if __name__ == "__main__":
    main()
