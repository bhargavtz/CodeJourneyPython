"""
CLI entry point for the Multi-Agent Team (Writer + Reviewer + Coordinator).

Usage (run from the repository root so the ``projects`` package resolves):
    python -m projects.ai_agents.agent3_multi_agent_team.main "your topic here"
"""

import sys

from dotenv import load_dotenv

from projects.utils.logging_config import setup_logger

from .coordinator import Coordinator


def main() -> None:
    """Run the Writer/Reviewer team on the topic passed on the command line."""
    load_dotenv()
    setup_logger(__name__, level="INFO")

    topic = " ".join(sys.argv[1:]) or "Why Python is a good first programming language"
    print(f"Topic: {topic}\n")

    coordinator = Coordinator()
    result = coordinator.run(topic)

    print(result.summary())
    print("--- Final draft ---")
    print(result.final_draft)


if __name__ == "__main__":
    main()
