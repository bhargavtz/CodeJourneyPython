"""
The two specialist agents the Coordinator manages.

Each is a thin wrapper around a single Anthropic call with its own system
prompt — deliberately simple, so the interesting part (how they're
orchestrated) stays in ``coordinator.py``.
"""

import logging
import os
import re
from typing import NamedTuple, Optional

from anthropic import Anthropic

logger = logging.getLogger(__name__)

DEFAULT_MODEL = os.getenv("AI_AGENTS_MODEL", "claude-sonnet-5")
DEFAULT_MAX_TOKENS = int(os.getenv("AI_AGENTS_MAX_TOKENS", "1024"))

WRITER_SYSTEM_PROMPT = (
    "You are a concise technical writer. Write a short (150-250 word) draft on the "
    "given topic. If revision feedback is provided, rewrite the draft to address it "
    "fully. Respond with ONLY the draft text, no preamble."
)

REVIEWER_SYSTEM_PROMPT = """\
You are a strict editor. Review the draft for clarity, accuracy, and whether it \
actually addresses the topic. Respond in exactly one of these two formats:

APPROVED

or

REVISE: <specific, actionable feedback for the writer>\
"""

_REVISE_RE = re.compile(r"REVISE:\s*(.*)", re.DOTALL)


class ReviewVerdict(NamedTuple):
    """The outcome of one review pass."""

    approved: bool
    feedback: Optional[str]


class WriterAgent:
    """Drafts (and revises) short pieces of writing on a topic."""

    def __init__(
        self, client: Anthropic, model: str = DEFAULT_MODEL, max_tokens: int = DEFAULT_MAX_TOKENS
    ):
        self.client = client
        self.model = model
        self.max_tokens = max_tokens

    def draft(self, topic: str, feedback: Optional[str] = None) -> str:
        """Produce a draft, optionally revising based on reviewer feedback.

        Args:
            topic: What to write about.
            feedback: Feedback from the ReviewerAgent's previous pass, if any.

        Returns:
            The draft text.
        """
        user_content = f"Topic: {topic}"
        if feedback:
            user_content += f"\n\nPrevious draft was rejected with this feedback:\n{feedback}"

        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=WRITER_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_content}],
        )
        draft = "".join(block.text for block in response.content if block.type == "text")
        logger.info("Writer produced a %d-character draft", len(draft))
        return draft.strip()


class ReviewerAgent:
    """Reviews a draft and either approves it or asks for specific changes."""

    def __init__(
        self, client: Anthropic, model: str = DEFAULT_MODEL, max_tokens: int = DEFAULT_MAX_TOKENS
    ):
        self.client = client
        self.model = model
        self.max_tokens = max_tokens

    def review(self, topic: str, draft: str) -> ReviewVerdict:
        """Review a draft against its topic.

        Args:
            topic: The topic the draft was supposed to cover.
            draft: The draft text to review.

        Returns:
            A ReviewVerdict indicating approval or the feedback to act on.
        """
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=REVIEWER_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": f"Topic: {topic}\n\nDraft:\n{draft}"}],
        )
        text = "".join(block.text for block in response.content if block.type == "text").strip()
        logger.info("Reviewer verdict: %s", text.splitlines()[0] if text else "<empty>")

        revise_match = _REVISE_RE.search(text)
        if revise_match:
            return ReviewVerdict(approved=False, feedback=revise_match.group(1).strip())
        return ReviewVerdict(approved=True, feedback=None)
