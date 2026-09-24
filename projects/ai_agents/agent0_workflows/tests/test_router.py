"""Offline tests for RouterWorkflow (Anthropic client mocked)."""

from unittest.mock import MagicMock, patch

import pytest

from projects.ai_agents.agent0_workflows.router import (
    DEFAULT_CATEGORY,
    ROUTE_SYSTEM_PROMPTS,
    RouterWorkflow,
    WorkflowError,
)


def _text_response(text):
    block = MagicMock()
    block.type = "text"
    block.text = text
    return MagicMock(content=[block])


class TestRouterWorkflowInit:
    def test_requires_api_key(self):
        with pytest.raises(WorkflowError):
            RouterWorkflow(api_key="")


class TestRouterWorkflowClassify:
    def _make_workflow(self, responses):
        with patch("projects.ai_agents.agent0_workflows.router.Anthropic") as mock_cls:
            client = MagicMock()
            client.messages.create.side_effect = [_text_response(r) for r in responses]
            mock_cls.return_value = client
            return RouterWorkflow(api_key="sk-test")

    def test_classify_recognizes_a_known_category(self):
        workflow = self._make_workflow(["billing"])
        assert workflow.classify("Why was I charged twice?") == "billing"

    def test_classify_is_case_insensitive(self):
        workflow = self._make_workflow(["  Technical  "])
        assert workflow.classify("It keeps crashing") == "technical"

    def test_classify_falls_back_to_default_on_unrecognized_output(self):
        workflow = self._make_workflow(["something the model made up"])
        assert workflow.classify("asdf") == DEFAULT_CATEGORY


class TestRouterWorkflowHandle:
    def _make_workflow(self, responses):
        with patch("projects.ai_agents.agent0_workflows.router.Anthropic") as mock_cls:
            client = MagicMock()
            client.messages.create.side_effect = [_text_response(r) for r in responses]
            mock_cls.return_value = client
            return RouterWorkflow(api_key="sk-test")

    def test_handle_uses_the_matching_system_prompt(self):
        workflow = self._make_workflow(["billing", "Let's look at your invoice."])

        result = workflow.handle("Why was I charged twice?")

        assert result.category == "billing"
        assert result.response == "Let's look at your invoice."
        second_call_kwargs = workflow.client.messages.create.call_args_list[1].kwargs
        assert second_call_kwargs["system"] == ROUTE_SYSTEM_PROMPTS["billing"]
