"""
Routing: classify the input with one small LLM call, then hand it to a
category-specific handler prompt. Still no loop, no tool use — just "pick a
lane, then run that lane's prompt" instead of one system prompt trying to be
good at everything at once.

This example routes a customer-support-style message into one of three
fixed categories. If the classifier ever returns something unrecognized,
`classify()` falls back to "general" rather than raising — a routing
mistake should degrade gracefully, not crash the workflow.
"""

import logging
import os
from dataclasses import dataclass
from typing import Optional

from anthropic import Anthropic

from projects.utils.errors import BaseProjectError

logger = logging.getLogger(__name__)

DEFAULT_MODEL = os.getenv("AI_AGENTS_MODEL", "claude-sonnet-5")
DEFAULT_MAX_TOKENS = int(os.getenv("AI_AGENTS_MAX_TOKENS", "1024"))

DEFAULT_CATEGORY = "general"

ROUTE_SYSTEM_PROMPTS = {
    "billing": (
        "You are a billing support specialist. Help with payments, invoices, "
        "refunds, and subscription changes. Be precise about amounts and dates."
    ),
    "technical": (
        "You are a technical support specialist. Help debug errors and explain "
        "how the product works. Ask a clarifying question if the report is vague."
    ),
    DEFAULT_CATEGORY: (
        "You are a friendly general support agent. Answer as best you can, and "
        "suggest the customer contact a specialist team if the topic needs one."
    ),
}

CLASSIFY_SYSTEM_PROMPT = (
    "Classify the user's message into exactly one of these categories: "
    f"{', '.join(ROUTE_SYSTEM_PROMPTS)}. Respond with ONLY the category word, nothing else."
)


class WorkflowError(BaseProjectError):
    """Raised when the workflow cannot run (e.g. missing API key)."""

    def __init__(self, message: str):
        super().__init__(message, "WORKFLOW_ERROR")


@dataclass
class RouteResult:
    """The outcome of routing and handling one message."""

    category: str
    response: str


class RouterWorkflow:
    """Classifies a message, then answers it with a category-specific prompt."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = DEFAULT_MODEL,
        max_tokens: int = DEFAULT_MAX_TOKENS,
    ):
        """Initialize the workflow.

        Args:
            api_key: Anthropic API key. Falls back to ANTHROPIC_API_KEY.
            model: Claude model identifier.
            max_tokens: Maximum tokens per model response.

        Raises:
            WorkflowError: If no API key is available.
        """
        api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise WorkflowError("ANTHROPIC_API_KEY is not set (env var or constructor arg).")

        self.client = Anthropic(api_key=api_key)
        self.model = model
        self.max_tokens = max_tokens

    def classify(self, message: str) -> str:
        """Classify a message into one of ROUTE_SYSTEM_PROMPTS's keys.

        Args:
            message: The user's message.

        Returns:
            A recognized category, falling back to DEFAULT_CATEGORY if the
            model's answer doesn't match one of the known categories.
        """
        raw = self._call(CLASSIFY_SYSTEM_PROMPT, message).strip().lower()
        if raw in ROUTE_SYSTEM_PROMPTS:
            return raw

        logger.warning("Unrecognized category %r; falling back to %r.", raw, DEFAULT_CATEGORY)
        return DEFAULT_CATEGORY

    def handle(self, message: str) -> RouteResult:
        """Classify a message, then answer it with that category's prompt.

        Args:
            message: The user's message.

        Returns:
            A RouteResult with the category used and the model's response.
        """
        category = self.classify(message)
        logger.info("Routed message to category: %s", category)

        response = self._call(ROUTE_SYSTEM_PROMPTS[category], message)
        return RouteResult(category=category, response=response)

    def _call(self, system_prompt: str, user_content: str) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_content}],
        )
        return "".join(block.text for block in response.content if block.type == "text")
