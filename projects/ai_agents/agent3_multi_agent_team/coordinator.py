"""
Coordinator: orchestrates the Writer/Reviewer team.

This is the "multi-agent" idea in its simplest form — two agents that never
talk to the user directly, only to each other, with a third piece of code
(not itself an LLM call) deciding when to stop and what "done" means.
"""

import logging
import os
from dataclasses import dataclass, field
from typing import List, Optional

from anthropic import Anthropic

from projects.utils.errors import BaseProjectError

from .agents import ReviewerAgent, WriterAgent

logger = logging.getLogger(__name__)

MAX_ROUNDS = 3


class CoordinatorError(BaseProjectError):
    """Raised when the team cannot be assembled (e.g. missing API key)."""

    def __init__(self, message: str):
        super().__init__(message, "COORDINATOR_ERROR")


@dataclass
class Round:
    """One writer-draft / reviewer-verdict cycle."""

    draft: str
    approved: bool
    feedback: Optional[str] = None


@dataclass
class TeamResult:
    """The outcome of running the whole team on a topic."""

    topic: str
    final_draft: str
    approved: bool
    rounds: List[Round] = field(default_factory=list)

    def summary(self) -> str:
        """Human-readable summary of how the team converged (or didn't)."""
        status = "APPROVED" if self.approved else "NOT APPROVED (max rounds reached)"
        return f"Topic: {self.topic}\n" f"Status: {status}\n" f"Rounds used: {len(self.rounds)}\n"


class Coordinator:
    """Runs the Writer -> Reviewer -> (revise?) loop until approval or MAX_ROUNDS."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the coordinator and its two team members.

        Args:
            api_key: Anthropic API key. Falls back to ANTHROPIC_API_KEY.

        Raises:
            CoordinatorError: If no API key is available.
        """
        api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise CoordinatorError("ANTHROPIC_API_KEY is not set (env var or constructor arg).")

        client = Anthropic(api_key=api_key)
        self.writer = WriterAgent(client)
        self.reviewer = ReviewerAgent(client)

    def run(self, topic: str) -> TeamResult:
        """Produce an approved draft on `topic`, or the best attempt after MAX_ROUNDS.

        Args:
            topic: What the team should write about.

        Returns:
            A TeamResult with the final draft, whether it was approved, and
            the full round-by-round history.
        """
        rounds: List[Round] = []
        feedback: Optional[str] = None
        draft = ""

        for round_number in range(1, MAX_ROUNDS + 1):
            draft = self.writer.draft(topic, feedback=feedback)
            verdict = self.reviewer.review(topic, draft)
            rounds.append(Round(draft=draft, approved=verdict.approved, feedback=verdict.feedback))

            logger.info(
                "Round %d/%d: %s",
                round_number,
                MAX_ROUNDS,
                "approved" if verdict.approved else "revise",
            )

            if verdict.approved:
                return TeamResult(topic=topic, final_draft=draft, approved=True, rounds=rounds)

            feedback = verdict.feedback

        return TeamResult(topic=topic, final_draft=draft, approved=False, rounds=rounds)
