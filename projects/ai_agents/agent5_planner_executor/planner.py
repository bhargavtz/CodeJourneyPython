"""
Planner: turns a high-level goal into an ordered list of concrete steps.

This is the piece the other four agents in this module don't have: instead
of reacting one turn at a time, the model commits to a full multi-step plan
up front, which ``executor.py`` then works through autonomously.
"""

import json
import logging
import os
import re
from dataclasses import dataclass
from typing import Any, List

from anthropic import Anthropic

logger = logging.getLogger(__name__)

DEFAULT_MODEL = os.getenv("AI_AGENTS_MODEL", "claude-sonnet-5")
DEFAULT_MAX_TOKENS = int(os.getenv("AI_AGENTS_MAX_TOKENS", "1024"))

AVAILABLE_TOOLS = ("note", "calculator", "write_file")

SYSTEM_PROMPT = f"""\
Break the user's goal down into 2-5 concrete steps. Respond with ONLY a JSON \
array (no prose, no markdown fences) where each element is:

  {{"description": "<what this step accomplishes>", \
"tool": "<one of: {', '.join(AVAILABLE_TOOLS)}>", "tool_input": "<input for that tool>"}}

Tool meanings:
  - note: record an observation or intermediate conclusion (tool_input = the text to record)
  - calculator: evaluate an arithmetic expression (tool_input = the expression)
  - write_file: save text as a step output file (tool_input = the file's content)
"""

_JSON_ARRAY_RE = re.compile(r"\[.*\]", re.DOTALL)


class PlanningError(Exception):
    """Raised when the model's plan cannot be parsed as valid steps."""


@dataclass
class Step:
    """A single planned step: what it's for, and which tool executes it."""

    description: str
    tool: str
    tool_input: str


class Planner:
    """Asks Claude to decompose a goal into a JSON list of Steps."""

    def __init__(
        self, client: Anthropic, model: str = DEFAULT_MODEL, max_tokens: int = DEFAULT_MAX_TOKENS
    ):
        self.client = client
        self.model = model
        self.max_tokens = max_tokens

    def plan(self, goal: str) -> List[Step]:
        """Decompose `goal` into an ordered list of Steps.

        Args:
            goal: The high-level goal to plan for.

        Returns:
            A list of Step objects, in execution order.

        Raises:
            PlanningError: If the model's response cannot be parsed as steps.
        """
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": f"Goal: {goal}"}],
        )
        text = "".join(block.text for block in response.content if block.type == "text")
        steps = self._parse_steps(text)
        logger.info("Planned %d step(s) for goal: %s", len(steps), goal)
        return steps

    @staticmethod
    def _parse_steps(text: str) -> List[Step]:
        """Extract a JSON array of steps from (possibly fenced) model output."""
        match = _JSON_ARRAY_RE.search(text)
        if not match:
            raise PlanningError(f"No JSON array found in planner output:\n{text}")

        try:
            raw_steps: List[Any] = json.loads(match.group(0))
        except json.JSONDecodeError as exc:
            raise PlanningError(f"Planner output was not valid JSON: {exc}") from exc

        steps = []
        for raw_step in raw_steps:
            try:
                steps.append(
                    Step(
                        description=raw_step["description"],
                        tool=raw_step["tool"],
                        tool_input=raw_step["tool_input"],
                    )
                )
            except (KeyError, TypeError) as exc:
                raise PlanningError(f"Malformed step in planner output: {raw_step}") from exc

        if not steps:
            raise PlanningError("Planner returned an empty step list.")
        return steps
