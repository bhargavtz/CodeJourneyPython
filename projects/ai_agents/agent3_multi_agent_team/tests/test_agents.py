"""Offline tests for WriterAgent and ReviewerAgent (Anthropic client mocked)."""

from unittest.mock import MagicMock

from projects.ai_agents.agent3_multi_agent_team.agents import ReviewerAgent, WriterAgent


def _text_response(text):
    block = MagicMock()
    block.type = "text"
    block.text = text
    return MagicMock(content=[block])


class TestWriterAgent:
    def test_draft_returns_stripped_text(self):
        client = MagicMock()
        client.messages.create.return_value = _text_response("  A short draft.  \n")

        writer = WriterAgent(client)
        draft = writer.draft("test topic")

        assert draft == "A short draft."

    def test_draft_includes_feedback_in_the_prompt(self):
        client = MagicMock()
        client.messages.create.return_value = _text_response("Revised draft.")

        writer = WriterAgent(client)
        writer.draft("test topic", feedback="Add an example.")

        sent_messages = client.messages.create.call_args.kwargs["messages"]
        assert "Add an example." in sent_messages[0]["content"]


class TestReviewerAgent:
    def test_approved_verdict(self):
        client = MagicMock()
        client.messages.create.return_value = _text_response("APPROVED")

        reviewer = ReviewerAgent(client)
        verdict = reviewer.review("topic", "draft")

        assert verdict.approved is True
        assert verdict.feedback is None

    def test_revise_verdict_extracts_feedback(self):
        client = MagicMock()
        client.messages.create.return_value = _text_response("REVISE: Add a conclusion.")

        reviewer = ReviewerAgent(client)
        verdict = reviewer.review("topic", "draft")

        assert verdict.approved is False
        assert verdict.feedback == "Add a conclusion."
