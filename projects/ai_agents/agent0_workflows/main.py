"""
CLI entry point for the two workflow demos: prompt chaining and routing.

Usage (run from the repository root so the ``projects`` package resolves):
    python -m projects.ai_agents.agent0_workflows.main chain "some long text" Spanish
    python -m projects.ai_agents.agent0_workflows.main route "My payment failed twice today"
"""

import sys

from dotenv import load_dotenv

from projects.utils.logging_config import setup_logger

from .prompt_chain import PromptChainWorkflow
from .router import RouterWorkflow

SAMPLE_TEXT = (
    "Python is a high-level, general-purpose programming language. Its design "
    "philosophy emphasizes code readability with the use of significant indentation. "
    "Python is dynamically typed and garbage-collected, and supports multiple "
    "programming paradigms, including structured, object-oriented, and functional "
    "programming."
)


def _run_chain(args) -> None:
    text = args[0] if args else SAMPLE_TEXT
    target_language = args[1] if len(args) > 1 else "French"

    workflow = PromptChainWorkflow()
    result = workflow.run(text, target_language)

    print(f"Summary: {result.summary}")
    if result.gate_passed:
        print(f"Translation ({target_language}): {result.translation}")
    else:
        print("Gate rejected the summary (too long) — translation step was skipped.")


def _run_router(args) -> None:
    message = " ".join(args) or "My payment failed twice today, can someone help?"

    workflow = RouterWorkflow()
    result = workflow.handle(message)

    print(f"Message: {message}")
    print(f"Routed to: {result.category}")
    print(f"Response: {result.response}")


def main() -> None:
    """Dispatch to the `chain` or `route` demo based on the first CLI argument."""
    load_dotenv()
    setup_logger(__name__, level="INFO")

    args = sys.argv[1:]
    command, rest = (
        (args[0], args[1:]) if args and args[0] in ("chain", "route") else ("chain", args)
    )

    if command == "chain":
        _run_chain(rest)
    else:
        _run_router(rest)


if __name__ == "__main__":
    main()
