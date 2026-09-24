"""Offline tests for MemoryAgent (Anthropic client mocked, real in-memory store)."""

from unittest.mock import MagicMock, patch

import pytest

from projects.ai_agents.agent4_memory_rag.agent import AgentError, MemoryAgent
from projects.ai_agents.agent4_memory_rag.memory_store import MemoryStore


def _text_response(text):
    block = MagicMock()
    block.type = "text"
    block.text = text
    return MagicMock(content=[block])


class TestMemoryAgentInit:
    def test_requires_api_key(self):
        with pytest.raises(AgentError):
            MemoryAgent(api_key="")

    def test_seeds_default_facts_when_store_is_empty(self):
        with patch("projects.ai_agents.agent4_memory_rag.agent.Anthropic"):
            empty_store = MemoryStore()
            agent = MemoryAgent(store=empty_store, api_key="sk-test")
            assert len(agent.store) > 0

    def test_does_not_reseed_a_populated_store(self):
        with patch("projects.ai_agents.agent4_memory_rag.agent.Anthropic"):
            store = MemoryStore()
            store.add("A single custom fact.")
            agent = MemoryAgent(store=store, api_key="sk-test")
            assert len(agent.store) == 1


class TestMemoryAgentAsk:
    def _make_agent(self, response_text):
        with patch("projects.ai_agents.agent4_memory_rag.agent.Anthropic") as mock_cls:
            client = MagicMock()
            client.messages.create.return_value = _text_response(response_text)
            mock_cls.return_value = client
            store = MemoryStore()
            store.add("The sky appears blue due to Rayleigh scattering.")
            return MemoryAgent(store=store, api_key="sk-test", seed_if_empty=False)

    def test_ask_returns_model_answer_when_context_found(self):
        agent = self._make_agent("The sky is blue because of Rayleigh scattering [1].")
        answer = agent.ask("Why is the sky blue?")
        assert "Rayleigh scattering" in answer

    def test_ask_short_circuits_when_nothing_relevant_is_stored(self):
        agent = self._make_agent("irrelevant")
        answer = agent.ask("Purple elephants dance loudly at midnight parties")
        assert "don't have any stored information" in answer

    def test_remember_adds_to_the_store(self):
        with patch("projects.ai_agents.agent4_memory_rag.agent.Anthropic"):
            store = MemoryStore()
            agent = MemoryAgent(store=store, api_key="sk-test", seed_if_empty=False)
            agent.remember("A brand new fact.")
            assert len(agent.store) == 1
