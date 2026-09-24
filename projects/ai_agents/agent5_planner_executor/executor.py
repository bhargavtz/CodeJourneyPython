"""
Executor: runs one planned Step against a small set of local tools.

No LLM calls happen here at all — this module is deliberately "dumb". All
the intelligence is in the Planner (deciding what to do) and, later, in the
agent's final summary (deciding what it all meant). The Executor just does
what it's told, and keeps a scratchpad of what happened.
"""

import logging
import math
from pathlib import Path
from typing import List, Optional

from .planner import Step

logger = logging.getLogger(__name__)


class ToolExecutionError(Exception):
    """Raised when a step's tool cannot be executed."""


class Executor:
    """Executes Steps using a small, fixed toolset and tracks a scratchpad."""

    def __init__(self, output_dir: Optional[str] = None):
        """Initialize the executor.

        Args:
            output_dir: Directory `write_file` steps save into. Created on
                first use if it doesn't exist. Defaults to an `outputs/`
                folder next to this file.
        """
        self.output_dir = Path(output_dir) if output_dir else Path(__file__).parent / "outputs"
        self.scratchpad: List[str] = []

    def execute_step(self, step: Step, step_number: int) -> str:
        """Run a single Step and record its result on the scratchpad.

        Args:
            step: The Step to execute.
            step_number: 1-based position of this step in the plan (used to
                name any files it writes).

        Returns:
            A human-readable result string for this step.
        """
        if step.tool == "note":
            result = self._note(step.tool_input)
        elif step.tool == "calculator":
            result = self._calculator(step.tool_input)
        elif step.tool == "write_file":
            result = self._write_file(step.tool_input, step_number)
        else:
            result = f"Error: unknown tool '{step.tool}'"

        entry = f"Step {step_number} ({step.description}): {result}"
        self.scratchpad.append(entry)
        logger.info(entry)
        return result

    def _note(self, text: str) -> str:
        """Record a plain observation. Just echoes it back for the scratchpad."""
        return text

    def _calculator(self, expression: str) -> str:
        """Safely evaluate an arithmetic expression."""
        allowed_names = {
            name: getattr(math, name) for name in dir(math) if not name.startswith("_")
        }
        allowed_names.update({"abs": abs, "round": round, "min": min, "max": max, "pow": pow})

        try:
            result = eval(expression, {"__builtins__": {}}, allowed_names)  # noqa: S307
        except Exception as exc:
            raise ToolExecutionError(f"Could not evaluate '{expression}': {exc}") from exc
        return str(result)

    def _write_file(self, content: str, step_number: int) -> str:
        """Write `content` to outputs/step_<n>.txt inside the sandboxed output dir."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        file_path = self.output_dir / f"step_{step_number}.txt"
        file_path.write_text(content)
        return f"Wrote {len(content)} characters to {file_path.name}"
