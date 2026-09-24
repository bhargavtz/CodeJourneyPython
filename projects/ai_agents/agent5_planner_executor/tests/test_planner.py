"""Offline tests for Planner's JSON step-parsing (Anthropic client mocked)."""

from unittest.mock import MagicMock

import pytest

from projects.ai_agents.agent5_planner_executor.planner import Planner, PlanningError, Step


def _text_response(text):
    block = MagicMock()
    block.type = "text"
    block.text = text
    return MagicMock(content=[block])


class TestPlannerParsing:
    def test_parses_plain_json_array(self):
        client = MagicMock()
        client.messages.create.return_value = _text_response(
            '[{"description": "Add numbers", "tool": "calculator", "tool_input": "2+2"}]'
        )
        planner = Planner(client)

        steps = planner.plan("add two numbers")

        assert steps == [Step(description="Add numbers", tool="calculator", tool_input="2+2")]

    def test_parses_json_wrapped_in_markdown_fences(self):
        client = MagicMock()
        client.messages.create.return_value = _text_response(
            '```json\n[{"description": "Note it", "tool": "note", "tool_input": "done"}]\n```'
        )
        planner = Planner(client)

        steps = planner.plan("do a thing")

        assert len(steps) == 1
        assert steps[0].tool == "note"

    def test_raises_on_missing_json(self):
        client = MagicMock()
        client.messages.create.return_value = _text_response("I refuse to make a plan.")
        planner = Planner(client)

        with pytest.raises(PlanningError):
            planner.plan("do a thing")

    def test_raises_on_malformed_step(self):
        client = MagicMock()
        client.messages.create.return_value = _text_response('[{"description": "missing tool"}]')
        planner = Planner(client)

        with pytest.raises(PlanningError):
            planner.plan("do a thing")

    def test_raises_on_empty_plan(self):
        client = MagicMock()
        client.messages.create.return_value = _text_response("[]")
        planner = Planner(client)

        with pytest.raises(PlanningError):
            planner.plan("do a thing")
