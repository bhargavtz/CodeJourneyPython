"""
WebSearchAgent: the fundamental agent loop.

The model decides *when* to call a tool, the tool runs locally, its output is
fed back to the model as a ``tool_result``, and the cycle repeats until the
model is confident enough to answer directly. This is the pattern almost
every other agent design (ReAct, planners, multi-agent systems) builds on.
"""

import json
import logging
import os
from typing import Any, Dict, List, Optional

from anthropic import Anthropic

from projects.utils.errors import BaseProjectError

from .search_tool import TOOL_SCHEMA, SearchError, web_search

logger = logging.getLogger(__name__)

DEFAULT_MODEL = os.getenv("AI_AGENTS_MODEL", "claude-sonnet-5")
DEFAULT_MAX_TOKENS = int(os.getenv("AI_AGENTS_MAX_TOKENS", "1024"))
MAX_TOOL_ROUNDS = 5


class AgentError(BaseProjectError):
    """Raised when the agent loop fails in an unrecoverable way."""

    def __init__(self, message: str):
        super().__init__(message, "AGENT_ERROR")


class WebSearchAgent:
    """An agent that can search the web to answer questions it isn't sure of."""

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
        self.system_prompt = (
            "You are a research assistant. Use the web_search tool whenever a "
            "question depends on facts you are not fully certain about. Cite "
            "the URLs you used at the end of your answer."
        )

    def ask(self, question: str) -> str:
        """Answer a question, calling the web_search tool as many times as needed.

        Args:
            question: The user's question.

        Returns:
            The agent's final natural-language answer.

        Raises:
            AgentError: If the loop does not converge within MAX_TOOL_ROUNDS.
        """
        messages: List[Dict[str, Any]] = [{"role": "user", "content": question}]

        for round_number in range(1, MAX_TOOL_ROUNDS + 1):
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=self.system_prompt,
                tools=[TOOL_SCHEMA],
                messages=messages,
            )

            messages.append({"role": "assistant", "content": response.content})

            if response.stop_reason != "tool_use":
                return self._extract_text(response.content)

            tool_results = [
                self._run_tool(block, round_number)
                for block in response.content
                if block.type == "tool_use"
            ]
            messages.append({"role": "user", "content": tool_results})

        raise AgentError(f"Agent did not converge after {MAX_TOOL_ROUNDS} tool-use rounds.")

    def _run_tool(self, block: Any, round_number: int) -> Dict[str, Any]:
        """Execute a single tool_use block and format it as a tool_result."""
        logger.info("Round %d: calling %s(%s)", round_number, block.name, block.input)

        try:
            if block.name == "web_search":
                results = web_search(**block.input)
                content = json.dumps([r.to_dict() for r in results])
            else:
                content = f"Unknown tool: {block.name}"
            is_error = False
        except SearchError as exc:
            content = str(exc)
            is_error = True

        return {
            "type": "tool_result",
            "tool_use_id": block.id,
            "content": content,
            "is_error": is_error,
        }

    @staticmethod
    def _extract_text(content_blocks: List[Any]) -> str:
        """Join the text blocks of a model response into a single string."""
        return "".join(block.text for block in content_blocks if block.type == "text")
