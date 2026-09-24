"""
Prompt chaining: a fixed sequence of small LLM calls with a plain-Python
"gate" check between them, instead of one big call trying to do everything.

There is no loop here and the model never decides what happens next — the
steps are hard-coded in ``PromptChainWorkflow.run()``. That predictability is
the whole point: chains are easy to test, easy to debug (you know exactly
which step produced a bad result), and cheaper to run than a full agent.
Reach for this before reaching for a loop.
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

SUMMARIZE_SYSTEM_PROMPT = (
    "Summarize the given text in one short paragraph. Respond with ONLY the summary."
)
TRANSLATE_SYSTEM_PROMPT_TEMPLATE = (
    "Translate the given text into {language}. Respond with ONLY the translation."
)


class WorkflowError(BaseProjectError):
    """Raised when the workflow cannot run (e.g. missing API key)."""

    def __init__(self, message: str):
        super().__init__(message, "WORKFLOW_ERROR")


@dataclass
class ChainResult:
    """The outcome of one prompt-chain run."""

    summary: str
    gate_passed: bool
    translation: Optional[str] = None


class PromptChainWorkflow:
    """Summarize a text, check the summary is short enough, then translate it."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = DEFAULT_MODEL,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        max_summary_words: int = 60,
    ):
        """Initialize the workflow.

        Args:
            api_key: Anthropic API key. Falls back to ANTHROPIC_API_KEY.
            model: Claude model identifier.
            max_tokens: Maximum tokens per model response.
            max_summary_words: The gate: if the summary is longer than this
                (by whitespace-split word count), the chain stops before
                spending a second call on translation.

        Raises:
            WorkflowError: If no API key is available.
        """
        api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise WorkflowError("ANTHROPIC_API_KEY is not set (env var or constructor arg).")

        self.client = Anthropic(api_key=api_key)
        self.model = model
        self.max_tokens = max_tokens
        self.max_summary_words = max_summary_words

    def run(self, text: str, target_language: str) -> ChainResult:
        """Run the chain: summarize -> gate check -> translate.

        Args:
            text: The source text to summarize and translate.
            target_language: The language to translate the summary into.

        Returns:
            A ChainResult. `translation` is None if the gate rejected the
            summary (in which case no second model call was made at all).
        """
        summary = self._call(SUMMARIZE_SYSTEM_PROMPT, text)

        if not self._passes_gate(summary):
            logger.info("Gate rejected summary (%d words); stopping chain.", len(summary.split()))
            return ChainResult(summary=summary, gate_passed=False)

        translate_prompt = TRANSLATE_SYSTEM_PROMPT_TEMPLATE.format(language=target_language)
        translation = self._call(translate_prompt, summary)
        return ChainResult(summary=summary, gate_passed=True, translation=translation)

    def _passes_gate(self, summary: str) -> bool:
        """The deterministic check between steps — no model call involved."""
        return bool(summary) and len(summary.split()) <= self.max_summary_words

    def _call(self, system_prompt: str, user_content: str) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_content}],
        )
        return "".join(block.text for block in response.content if block.type == "text").strip()
