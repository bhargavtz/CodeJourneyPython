"""Offline tests for PromptChainWorkflow (Anthropic client mocked)."""

from unittest.mock import MagicMock, patch

import pytest

from projects.ai_agents.agent0_workflows.prompt_chain import PromptChainWorkflow, WorkflowError


def _text_response(text):
    block = MagicMock()
    block.type = "text"
    block.text = text
    return MagicMock(content=[block])


class TestPromptChainWorkflowInit:
    def test_requires_api_key(self):
        with pytest.raises(WorkflowError):
            PromptChainWorkflow(api_key="")


class TestPromptChainWorkflowRun:
    def _make_workflow(self, responses, **kwargs):
        with patch("projects.ai_agents.agent0_workflows.prompt_chain.Anthropic") as mock_cls:
            client = MagicMock()
            client.messages.create.side_effect = [_text_response(r) for r in responses]
            mock_cls.return_value = client
            return PromptChainWorkflow(api_key="sk-test", **kwargs)

    def test_gate_passes_and_chain_completes(self):
        workflow = self._make_workflow(["A short summary.", "Un resume court."])

        result = workflow.run("some long text", "French")

        assert result.gate_passed is True
        assert result.summary == "A short summary."
        assert result.translation == "Un resume court."
        assert workflow.client.messages.create.call_count == 2

    def test_gate_rejects_long_summary_and_skips_translation(self):
        long_summary = " ".join(["word"] * 100)
        workflow = self._make_workflow([long_summary], max_summary_words=60)

        result = workflow.run("some long text", "French")

        assert result.gate_passed is False
        assert result.translation is None
        # Only the summarize call happened -- the gate stopped the chain
        # before a second (translation) call was ever made.
        assert workflow.client.messages.create.call_count == 1

    def test_gate_rejects_empty_summary(self):
        workflow = self._make_workflow([""])

        result = workflow.run("some long text", "French")

        assert result.gate_passed is False
        assert result.translation is None
