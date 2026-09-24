"""
ReActAgent: the agent loop implemented by hand, with no ``tools=`` parameter.

This is the ReAct pattern (Reason + Act) from Yao et al., 2022: the model is
prompted to interleave free-text "Thought" / "Action" / "Observation" turns
until it emits a "Final Answer". Compare this file to
``agent1_web_search/agent.py`` — same idea, no SDK tool-calling support
required, which is useful when you're working with a model or API that
doesn't offer native tool use.
"""

import logging
import os
import re
from typing import List, Optional

from anthropic import Anthropic

from projects.utils.errors import BaseProjectError

from .tools import TOOL_DESCRIPTIONS, TOOLS, ToolExecutionError

logger = logging.getLogger(__name__)

DEFAULT_MODEL = os.getenv("AI_AGENTS_MODEL", "claude-sonnet-5")
DEFAULT_MAX_TOKENS = int(os.getenv("AI_AGENTS_MAX_TOKENS", "1024"))
MAX_STEPS = 6

_ACTION_RE = re.compile(r"Action:\s*(\w+)\[(.*?)\]", re.DOTALL)
_FINAL_ANSWER_RE = re.compile(r"Final Answer:\s*(.*)", re.DOTALL)

SYSTEM_PROMPT = f"""\
You solve problems by reasoning step by step using this exact format:

Thought: <your reasoning about what to do next>
Action: <tool_name>[<tool_input>]

Available tools:
{TOOL_DESCRIPTIONS}

After an Action, you will be given an Observation with the tool's result.
Keep alternating Thought/Action/Observation until you can answer. When you
are ready to answer, respond with exactly:

Thought: <final reasoning>
Final Answer: <your answer>

Only ever emit ONE Thought and ONE Action (or Final Answer) per turn.\
"""


class AgentError(BaseProjectError):
    """Raised when the ReAct loop fails to produce a final answer."""

    def __init__(self, message: str):
        super().__init__(message, "AGENT_ERROR")


class ReActAgent:
    """An agent that reasons in plain text and calls tools by parsing its own output."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = DEFAULT_MODEL,
        max_tokens: int = DEFAULT_MAX_TOKENS,
    ):
        """Initialize the agent.

        Args:
            api_key: Anthropic API key. Falls back to ANTHROPIC_API_KEY.
            model: Claude model identifier.
            max_tokens: Maximum tokens per model response.

        Raises:
            AgentError: If no API key is available.
        """
        api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise AgentError("ANTHROPIC_API_KEY is not set (env var or constructor arg).")

        self.client = Anthropic(api_key=api_key)
        self.model = model
        self.max_tokens = max_tokens

    def run(self, question: str) -> str:
        """Solve a question with a Thought/Action/Observation loop.

        Args:
            question: The question or task to solve.

        Returns:
            The text following "Final Answer:".

        Raises:
            AgentError: If MAX_STEPS is exceeded without a final answer.
        """
        transcript: List[str] = [f"Question: {question}"]

        for step in range(1, MAX_STEPS + 1):
            completion = self._call_model("\n".join(transcript))
            logger.debug("Step %d model output:\n%s", step, completion)

            final_match = _FINAL_ANSWER_RE.search(completion)
            if final_match:
                return final_match.group(1).strip()

            action_match = _ACTION_RE.search(completion)
            if not action_match:
                transcript.append(completion)
                transcript.append(
                    "Observation: Your last turn had no Action or Final Answer. "
                    "Follow the required format exactly."
                )
                continue

            tool_name, tool_input = action_match.group(1), action_match.group(2).strip()
            observation = self._run_tool(tool_name, tool_input)

            transcript.append(completion)
            transcript.append(f"Observation: {observation}")

        raise AgentError(f"No Final Answer after {MAX_STEPS} steps.")

    def _call_model(self, user_content: str) -> str:
        """Send the running transcript to Claude and return its raw text reply."""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_content}],
        )
        return "".join(block.text for block in response.content if block.type == "text")

    @staticmethod
    def _run_tool(tool_name: str, tool_input: str) -> str:
        """Dispatch to a local tool by name, returning a human-readable observation."""
        tool_fn = TOOLS.get(tool_name)
        if tool_fn is None:
            return f"Error: unknown tool '{tool_name}'."

        try:
            return tool_fn(tool_input)
        except ToolExecutionError as exc:
            return f"Error: {exc}"
