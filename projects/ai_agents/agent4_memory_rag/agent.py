"""
MemoryAgent: retrieval-augmented generation on top of MemoryStore.

The agent never lets the model answer from its own general knowledge —
the system prompt instructs it to use *only* the retrieved context, and to
say so plainly when the context doesn't contain the answer. That's the core
guarantee RAG is meant to provide: answers you can trace back to a source.
"""

import logging
import os
from typing import List, Optional

from anthropic import Anthropic

from projects.utils.errors import BaseProjectError

from .memory_store import MemoryStore

logger = logging.getLogger(__name__)

DEFAULT_MODEL = os.getenv("AI_AGENTS_MODEL", "claude-sonnet-5")
DEFAULT_MAX_TOKENS = int(os.getenv("AI_AGENTS_MAX_TOKENS", "1024"))
DEFAULT_TOP_K = 3

SYSTEM_PROMPT = (
    "Answer the user's question using ONLY the numbered context passages below. "
    "Cite the passage number(s) you used, like [1]. If the passages don't contain "
    "the answer, say plainly that you don't have enough information — do not use "
    "outside knowledge."
)

# A few facts about this repository so the demo is useful with zero setup.
DEFAULT_SEED_FACTS = [
    "CodeJourneyPython is a Python learning platform organized into projects/, "
    "libraries/, and resources/ folders.",
    "Shared conventions live in projects/utils/: config.py, errors.py, and "
    "logging_config.py, which every project is expected to reuse.",
    "projects/ai_agents/ contains five educational agent implementations: "
    "web search (tool use), ReAct reasoning, a multi-agent writer/reviewer team, "
    "this memory/RAG agent, and a planner-executor agent.",
]


class AgentError(BaseProjectError):
    """Raised when the agent cannot answer (e.g. missing API key)."""

    def __init__(self, message: str):
        super().__init__(message, "AGENT_ERROR")


class MemoryAgent:
    """An agent that answers questions grounded in documents it was told to remember."""

    def __init__(
        self,
        store: Optional[MemoryStore] = None,
        api_key: Optional[str] = None,
        model: str = DEFAULT_MODEL,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        top_k: int = DEFAULT_TOP_K,
        seed_if_empty: bool = True,
    ):
        """Initialize the agent.

        Args:
            store: A MemoryStore to use. A fresh in-memory one is created if omitted.
            api_key: Anthropic API key. Falls back to ANTHROPIC_API_KEY.
            model: Claude model identifier.
            max_tokens: Maximum tokens per model response.
            top_k: How many retrieved passages to include as context.
            seed_if_empty: If True and the store has no documents, load
                DEFAULT_SEED_FACTS so the agent is useful immediately.

        Raises:
            AgentError: If no API key is available.
        """
        api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise AgentError("ANTHROPIC_API_KEY is not set (env var or constructor arg).")

        self.client = Anthropic(api_key=api_key)
        self.model = model
        self.max_tokens = max_tokens
        self.top_k = top_k
        self.store = store if store is not None else MemoryStore()

        if seed_if_empty and len(self.store) == 0:
            for fact in DEFAULT_SEED_FACTS:
                self.store.add(fact)

    def remember(self, text: str) -> str:
        """Store a new fact for later retrieval.

        Args:
            text: The text to remember.

        Returns:
            The id assigned to the stored document.
        """
        return self.store.add(text)

    def ask(self, question: str) -> str:
        """Answer a question using only retrieved context passages.

        Args:
            question: The user's question.

        Returns:
            The model's answer, grounded in the retrieved passages.
        """
        matches = self.store.search(question, top_k=self.top_k)

        if not matches:
            return "I don't have any stored information relevant to that question."

        context = self._format_context(matches)
        logger.info("Retrieved %d passage(s) for question: %s", len(matches), question)

        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": f"{context}\n\nQuestion: {question}"}],
        )
        return "".join(block.text for block in response.content if block.type == "text")

    @staticmethod
    def _format_context(matches: List) -> str:
        """Render retrieved (Document, score) pairs as numbered context passages."""
        lines = []
        for index, (doc, score) in enumerate(matches, start=1):
            lines.append(f"[{index}] (similarity={score:.2f}) {doc.text}")
        return "\n".join(lines)
