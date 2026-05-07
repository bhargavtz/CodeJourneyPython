"""
Unit tests for AI Agent implementation.

Tests core agent functionality including:
- Agent initialization
- Conversation management
- Error handling
- State tracking

Author: CodeJourney AI Project
License: MIT
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from agent import AIAgent, ConversationState, Message


class TestMessage:
    """Test Message dataclass."""

    def test_message_creation(self):
        """Test creating a message."""
        msg = Message("user", "Hello")
        assert msg.role == "user"
        assert msg.content == "Hello"
        assert msg.tokens == 0

    def test_message_to_dict(self):
        """Test converting message to dict."""
        msg = Message("assistant", "Hi there")
        result = msg.to_dict()
        assert result == {"role": "assistant", "content": "Hi there"}


class TestConversationState:
    """Test ConversationState class."""

    def test_state_initialization(self):
        """Test state starts empty."""
        state = ConversationState()
        assert len(state.messages) == 0
        assert state.total_tokens == 0
        assert state.tool_uses == 0

    def test_add_message(self):
        """Test adding messages."""
        state = ConversationState()
        state.add_message("user", "Hello", tokens=10)
        assert len(state.messages) == 1
        assert state.total_tokens == 10

    def test_clear_state(self):
        """Test clearing state."""
        state = ConversationState()
        state.add_message("user", "Test")
        state.total_tokens = 100
        state.clear()
        assert len(state.messages) == 0
        assert state.total_tokens == 0

    def test_get_history(self):
        """Test getting conversation history."""
        state = ConversationState()
        state.add_message("user", "Hi")
        state.add_message("assistant", "Hello")
        history = state.get_history()
        assert len(history) == 2
        assert history[0]["role"] == "user"


class TestAIAgent:
    """Test AIAgent class."""

    @pytest.fixture
    def mock_api_key(self):
        """Mock API key."""
        return "sk-test-key"

    @pytest.fixture
    def agent(self, mock_api_key):
        """Create agent instance with mocked API."""
        with patch("agent.Anthropic"):
            agent = AIAgent(api_key=mock_api_key)
            agent.client = MagicMock()
            return agent

    def test_agent_initialization(self, agent):
        """Test agent initialization."""
        assert agent.model == "claude-opus-4-7"
        assert agent.max_tokens == 2048
        assert agent.system_prompt is not None

    def test_invalid_api_key(self):
        """Test that empty API key raises error."""
        with pytest.raises(ValueError):
            AIAgent(api_key="")

    def test_register_tools(self, agent):
        """Test registering tools."""
        tools = [{"name": "test", "description": "Test tool"}]
        agent.register_tools(tools)
        assert len(agent.tools) == 1

    def test_clear_conversation(self, agent):
        """Test clearing conversation."""
        agent.state.add_message("user", "Test")
        agent.clear_conversation()
        assert len(agent.state.messages) == 0

    def test_get_conversation_history(self, agent):
        """Test getting conversation history."""
        agent.state.add_message("user", "Hi")
        agent.state.add_message("assistant", "Hello")
        history = agent.get_conversation_history()
        assert len(history) == 2

    def test_set_system_prompt(self, agent):
        """Test updating system prompt."""
        new_prompt = "You are a helpful assistant"
        agent.set_system_prompt(new_prompt)
        assert agent.system_prompt == new_prompt

    def test_get_statistics(self, agent):
        """Test getting statistics."""
        agent.state.add_message("user", "Test", tokens=10)
        stats = agent.get_statistics()
        assert "Messages: 1" in stats
        assert "Total Tokens: 10" in stats

    @patch("builtins.open", create=True)
    def test_save_conversation(self, mock_open, agent):
        """Test saving conversation."""
        agent.state.add_message("user", "Hi")
        agent.state.add_message("assistant", "Hello")

        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file

        agent.save_conversation("test.json")
        mock_open.assert_called_once()

    @patch("builtins.open", create=True)
    def test_load_conversation(self, mock_open, agent):
        """Test loading conversation."""
        mock_file = MagicMock()
        mock_file.read.return_value = '{"messages": [{"role": "user", "content": "Hi"}]}'
        mock_open.return_value.__enter__.return_value = mock_file

        # Mock json.load
        with patch("json.load") as mock_json:
            mock_json.return_value = {
                "messages": [{"role": "user", "content": "Hi"}]
            }
            agent.load_conversation("test.json")


class TestAgentChat:
    """Test chat functionality."""

    @pytest.fixture
    def agent_with_mock_api(self):
        """Agent with mocked API responses."""
        with patch("agent.Anthropic") as mock_anthropic:
            mock_instance = MagicMock()

            # Mock response
            mock_response = MagicMock()
            mock_response.content = [MagicMock(text="Hello! How can I help?")]
            mock_instance.messages.create.return_value = mock_response

            mock_anthropic.return_value = mock_instance

            agent = AIAgent(api_key="test-key")
            return agent

    def test_chat_basic_interaction(self, agent_with_mock_api):
        """Test basic chat interaction."""
        response = agent_with_mock_api.chat("Hello")
        assert isinstance(response, str)
        assert len(agent_with_mock_api.state.messages) == 2

    def test_chat_adds_to_history(self, agent_with_mock_api):
        """Test that messages are added to history."""
        agent_with_mock_api.chat("Hello")
        history = agent_with_mock_api.get_conversation_history()
        assert history[0]["role"] == "user"
        assert history[1]["role"] == "assistant"

    def test_chat_multiple_turns(self, agent_with_mock_api):
        """Test multiple conversation turns."""
        agent_with_mock_api.chat("Hello")
        agent_with_mock_api.chat("How are you?")
        history = agent_with_mock_api.get_conversation_history()
        assert len(history) == 4


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
