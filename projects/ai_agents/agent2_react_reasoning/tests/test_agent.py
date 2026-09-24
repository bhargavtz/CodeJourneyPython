"""Offline tests for the ReAct loop (Anthropic client mocked)."""

from unittest.mock import MagicMock, patch

import pytest

from projects.ai_agents.agent2_react_reasoning.agent import AgentError, ReActAgent


def _completion(text):
    """Build a fake Anthropic response whose only content block is `text`."""
    block = MagicMock()
    block.type = "text"
    block.text = text
    return MagicMock(content=[block])


class TestReActAgentInit:
    def test_requires_api_key(self):
        with pytest.raises(AgentError):
            ReActAgent(api_key="")


class TestReActAgentRun:
    def _make_agent(self, completions):
        with patch("projects.ai_agents.agent2_react_reasoning.agent.Anthropic") as mock_cls:
            client = MagicMock()
            client.messages.create.side_effect = [_completion(c) for c in completions]
            mock_cls.return_value = client
            return ReActAgent(api_key="sk-test")

    def test_answers_immediately(self):
        agent = self._make_agent(["Thought: easy\nFinal Answer: 42"])
        assert agent.run("What is 6*7?") == "42"

    def test_runs_a_tool_then_answers(self):
        agent = self._make_agent(
            [
                "Thought: I should look it up\nAction: knowledge_lookup[capital of france]",
                "Thought: Now I know\nFinal Answer: Paris",
            ]
        )
        answer = agent.run("What is the capital of France?")
        assert answer == "Paris"

    def test_unknown_tool_becomes_an_observation_not_a_crash(self):
        agent = self._make_agent(
            [
                "Thought: try a bogus tool\nAction: teleport[nowhere]",
                "Thought: that failed, give up gracefully\nFinal Answer: I cannot do that.",
            ]
        )
        answer = agent.run("Teleport me somewhere.")
        assert answer == "I cannot do that."

    def test_raises_after_max_steps_without_final_answer(self):
        # Every turn is malformed (no Action, no Final Answer) -> loop exhausts MAX_STEPS.
        agent = self._make_agent(["Thought: hmm"] * 10)
        with pytest.raises(AgentError):
            agent.run("Confuse the agent")
