"""Offline tests for WebSearchAgent's tool-use loop (Anthropic client mocked)."""

from unittest.mock import MagicMock, patch

import pytest

from projects.ai_agents.agent1_web_search.agent import AgentError, WebSearchAgent


def _text_block(text):
    block = MagicMock()
    block.type = "text"
    block.text = text
    return block


def _tool_use_block(name, tool_input, tool_id="tool_1"):
    block = MagicMock()
    block.type = "tool_use"
    block.name = name
    block.input = tool_input
    block.id = tool_id
    return block


class TestWebSearchAgentInit:
    def test_requires_api_key(self):
        with pytest.raises(AgentError):
            WebSearchAgent(api_key="")

    def test_accepts_explicit_api_key(self):
        with patch("projects.ai_agents.agent1_web_search.agent.Anthropic"):
            agent = WebSearchAgent(api_key="sk-test")
            assert agent.model
            assert agent.max_tokens > 0


class TestWebSearchAgentAsk:
    def _make_agent(self, responses):
        with patch("projects.ai_agents.agent1_web_search.agent.Anthropic") as mock_anthropic:
            client = MagicMock()
            client.messages.create.side_effect = responses
            mock_anthropic.return_value = client
            return WebSearchAgent(api_key="sk-test")

    def test_answers_directly_without_tool_use(self):
        direct_response = MagicMock(stop_reason="end_turn", content=[_text_block("42")])
        agent = self._make_agent([direct_response])

        answer = agent.ask("What is 6 * 7?")
        assert answer == "42"

    def test_calls_tool_then_answers(self):
        tool_call_response = MagicMock(
            stop_reason="tool_use",
            content=[_tool_use_block("web_search", {"query": "latest python version"})],
        )
        final_response = MagicMock(
            stop_reason="end_turn", content=[_text_block("Python 3.13 is the latest release.")]
        )
        agent = self._make_agent([tool_call_response, final_response])

        with patch(
            "projects.ai_agents.agent1_web_search.agent.web_search", return_value=[]
        ) as mock_search:
            answer = agent.ask("What is the latest Python version?")

        mock_search.assert_called_once_with(query="latest python version")
        assert "3.13" in answer

    def test_raises_if_it_never_converges(self):
        looping_response = MagicMock(
            stop_reason="tool_use",
            content=[_tool_use_block("web_search", {"query": "x"})],
        )
        agent = self._make_agent([looping_response] * 10)

        with patch("projects.ai_agents.agent1_web_search.agent.web_search", return_value=[]):
            with pytest.raises(AgentError):
                agent.ask("Never-ending question")
