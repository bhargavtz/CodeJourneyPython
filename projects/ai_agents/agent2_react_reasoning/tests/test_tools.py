"""Offline tests for the ReAct agent's local tools."""

import pytest

from projects.ai_agents.agent2_react_reasoning.tools import (
    ToolExecutionError,
    calculator,
    knowledge_lookup,
)


class TestCalculator:
    def test_basic_arithmetic(self):
        assert calculator("2 + 2") == "4"

    def test_uses_math_functions(self):
        assert calculator("sqrt(16)") == "4.0"

    def test_division_by_zero_raises(self):
        with pytest.raises(ToolExecutionError):
            calculator("1 / 0")

    def test_invalid_expression_raises(self):
        with pytest.raises(ToolExecutionError):
            calculator("import os")


class TestKnowledgeLookup:
    def test_known_topic_is_case_insensitive(self):
        assert knowledge_lookup("Capital Of France") == "Paris"

    def test_unknown_topic_returns_message(self):
        result = knowledge_lookup("capital of atlantis")
        assert "No local knowledge" in result
