"""
PlannerExecutorAgent: plan a goal, execute every step, then summarize.

The autonomy here is bounded on purpose: the plan is generated once, up
front, and then simply worked through — there's no re-planning loop like
Agents 1 and 2 have. That tradeoff (predictable, easy to audit, but unable
to adapt mid-run) is exactly what the README's "Things to try next" section
asks you to poke at.
"""

import logging
import os
from dataclasses import dataclass, field
from typing import List, Optional

from anthropic import Anthropic

from projects.utils.errors import BaseProjectError

from .executor import Executor
from .planner import Planner, Step

logger = logging.getLogger(__name__)

DEFAULT_MODEL = os.getenv("AI_AGENTS_MODEL", "claude-sonnet-5")
DEFAULT_MAX_TOKENS = int(os.getenv("AI_AGENTS_MAX_TOKENS", "1024"))

SUMMARY_SYSTEM_PROMPT = (
    "You are summarizing the work an autonomous agent just completed. Given the "
    "original goal and the results of each step it executed, write a 2-4 sentence "
    "summary of what was accomplished, in plain language for the person who set the goal."
)


class AgentError(BaseProjectError):
    """Raised when the agent cannot run (e.g. missing API key)."""

    def __init__(self, message: str):
        super().__init__(message, "AGENT_ERROR")


@dataclass
class RunResult:
    """Everything produced by one PlannerExecutorAgent.run() call."""

    goal: str
    plan: List[Step]
    step_results: List[str] = field(default_factory=list)
    summary: str = ""


class PlannerExecutorAgent:
    """Plans a goal into steps, executes them, then summarizes the outcome."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = DEFAULT_MODEL,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        output_dir: Optional[str] = None,
    ):
        """Initialize the agent.

        Args:
            api_key: Anthropic API key. Falls back to ANTHROPIC_API_KEY.
            model: Claude model identifier.
            max_tokens: Maximum tokens per model response.
            output_dir: Where `write_file` steps save their output.

        Raises:
            AgentError: If no API key is available.
        """
        api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise AgentError("ANTHROPIC_API_KEY is not set (env var or constructor arg).")

        self.client = Anthropic(api_key=api_key)
        self.model = model
        self.max_tokens = max_tokens
        self.planner = Planner(self.client, model=model, max_tokens=max_tokens)
        self.executor = Executor(output_dir=output_dir)

    def run(self, goal: str) -> RunResult:
        """Plan, execute, and summarize a run against `goal`.

        Args:
            goal: The high-level goal to accomplish.

        Returns:
            A RunResult with the plan, each step's result, and a final summary.
        """
        plan = self.planner.plan(goal)

        step_results = [
            self.executor.execute_step(step, step_number)
            for step_number, step in enumerate(plan, start=1)
        ]

        summary = self._summarize(goal, plan, step_results)
        return RunResult(goal=goal, plan=plan, step_results=step_results, summary=summary)

    def _summarize(self, goal: str, plan: List[Step], step_results: List[str]) -> str:
        """Ask Claude to summarize the completed run in plain language."""
        report_lines = [
            f"{i}. {step.description} -> {result}"
            for i, (step, result) in enumerate(zip(plan, step_results), start=1)
        ]
        report = "\n".join(report_lines)

        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=SUMMARY_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": f"Goal: {goal}\n\nStep results:\n{report}"}],
        )
        return "".join(block.text for block in response.content if block.type == "text")
