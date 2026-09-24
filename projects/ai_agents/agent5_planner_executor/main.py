"""
CLI entry point for the Planner-Executor Agent.

Usage (run from the repository root so the ``projects`` package resolves):
    python -m projects.ai_agents.agent5_planner_executor.main "your goal here"
"""

import sys

from dotenv import load_dotenv

from projects.utils.logging_config import setup_logger

from .agent import PlannerExecutorAgent


def main() -> None:
    """Plan, execute, and summarize a run against the goal on the command line."""
    load_dotenv()
    setup_logger(__name__, level="INFO")

    goal = " ".join(sys.argv[1:]) or (
        "Explain what a 20% tip on a $45.50 bill is, and save the explanation to a file."
    )
    print(f"Goal: {goal}\n")

    agent = PlannerExecutorAgent()
    result = agent.run(goal)

    print("--- Plan ---")
    for i, step in enumerate(result.plan, start=1):
        print(f"{i}. [{step.tool}] {step.description}")

    print("\n--- Step results ---")
    for i, step_result in enumerate(result.step_results, start=1):
        print(f"{i}. {step_result}")

    print("\n--- Summary ---")
    print(result.summary)


if __name__ == "__main__":
    main()
