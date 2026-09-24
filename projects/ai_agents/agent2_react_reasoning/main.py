"""
CLI entry point for the ReAct Reasoning Agent.

Usage (run from the repository root so the ``projects`` package resolves):
    python -m projects.ai_agents.agent2_react_reasoning.main "your question here"
"""

import sys

from dotenv import load_dotenv

from projects.utils.logging_config import setup_logger

from .agent import ReActAgent


def main() -> None:
    """Solve the question passed on the command line."""
    load_dotenv()
    setup_logger(__name__, level="INFO")

    question = " ".join(sys.argv[1:]) or "What is the capital of France, and what is 12 * 8?"
    print(f"Q: {question}\n")

    agent = ReActAgent()
    print(agent.run(question))


if __name__ == "__main__":
    main()
