"""
Unit tests for AI Agent implementation.

Tests core agent functionality including:
- Agent initialization
- Conversation management
- Tool execution
- Error handling
- State tracking

Author: CodeJourney AI Project
License: MIT
"""

from unittest.mock import MagicMock, patch

import pytest

from projects.ai_agent_chatbot.agent import AIAgent, ConversationState, Message


def _text_block(text):
    """Build a fake Anthropic content block that is text-only."""
    return MagicMock(type="text", text=text)


def _tool_use_block(name, tool_input, tool_id="tool_1"):
    """Build a fake Anthropic content block requesting a tool call.

    Note: ``name`` can't be passed as a MagicMock constructor kwarg -- that
    sets the mock's internal debug name, not a ``.name`` attribute -- so it
    has to be assigned afterward.
    """
    block = MagicMock(type="tool_use", input=tool_input, id=tool_id)
    block.name = name
    return block


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
        with patch("projects.ai_agent_chatbot.agent.Anthropic"):
            agent = AIAgent(api_key=mock_api_key)
            agent.client = MagicMock()
            return agent

    def test_agent_initialization(self, agent):
        """Test agent initialization."""
        assert agent.model == "claude-opus-4-7"
        assert agent.max_tokens == 2048
        assert agent.system_prompt is not None
        assert agent.tool_executor is None

    def test_invalid_api_key(self):
        """Test that empty API key raises error."""
        with pytest.raises(ValueError):
            AIAgent(api_key="")

    def test_register_tools_without_executor(self, agent):
        """Test registering tools without an executor (backwards compatible)."""
        tools = [{"name": "test", "description": "Test tool"}]
        agent.register_tools(tools)
        assert len(agent.tools) == 1
        assert agent.tool_executor is None

    def test_register_tools_with_executor(self, agent):
        """Test registering tools together with their executor."""
        tools = [{"name": "test", "description": "Test tool"}]
        executor = MagicMock(return_value="42")
        agent.register_tools(tools, executor=executor)
        assert agent.tool_executor is executor

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
            mock_json.return_value = {"messages": [{"role": "user", "content": "Hi"}]}
            agent.load_conversation("test.json")


class TestAgentChat:
    """Test chat functionality."""

    @pytest.fixture
    def agent_with_mock_api(self):
        """Agent with mocked API responses."""
        with patch("projects.ai_agent_chatbot.agent.Anthropic") as mock_anthropic:
            mock_instance = MagicMock()

            # Mock response
            mock_response = MagicMock(content=[_text_block("Hello! How can I help?")])
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

    def test_chat_executes_a_requested_tool(self):
        """A tool_use response should actually run the registered executor."""
        with patch("projects.ai_agent_chatbot.agent.Anthropic") as mock_anthropic:
            client = MagicMock()
            tool_call_response = MagicMock(
                content=[_tool_use_block("calculator", {"expression": "2 + 2"})]
            )
            final_response = MagicMock(content=[_text_block("2 + 2 = 4")])
            client.messages.create.side_effect = [tool_call_response, final_response]
            mock_anthropic.return_value = client

            agent = AIAgent(api_key="test-key")
            executor = MagicMock(return_value="2 + 2 = 4")
            agent.register_tools([{"name": "calculator"}], executor=executor)

            response = agent.chat("What is 2 + 2?")

        executor.assert_called_once_with("calculator", expression="2 + 2")
        assert response == "2 + 2 = 4"
        assert agent.state.tool_uses == 1

    def test_chat_reports_missing_executor_to_the_model(self):
        """If a tool is requested but no executor is registered, the model
        should be told so (as a tool_result) instead of the agent crashing."""
        with patch("projects.ai_agent_chatbot.agent.Anthropic") as mock_anthropic:
            client = MagicMock()
            tool_call_response = MagicMock(
                content=[_tool_use_block("calculator", {"expression": "2 + 2"})]
            )
            final_response = MagicMock(content=[_text_block("I couldn't run that tool.")])
            client.messages.create.side_effect = [tool_call_response, final_response]
            mock_anthropic.return_value = client

            agent = AIAgent(api_key="test-key")
            agent.register_tools([{"name": "calculator"}])  # no executor

            response = agent.chat("What is 2 + 2?")

        second_call_messages = client.messages.create.call_args_list[1].kwargs["messages"]
        tool_result_content = second_call_messages[-1]["content"][0]["content"]
        assert "no tool executor registered" in tool_result_content
        assert response == "I couldn't run that tool."

    def test_chat_gives_up_after_max_tool_rounds(self):
        """The agent should not loop forever if the model keeps calling tools."""
        with patch("projects.ai_agent_chatbot.agent.Anthropic") as mock_anthropic:
            client = MagicMock()
            looping_response = MagicMock(
                content=[_tool_use_block("calculator", {"expression": "1 + 1"})]
            )
            client.messages.create.return_value = looping_response
            mock_anthropic.return_value = client

            agent = AIAgent(api_key="test-key")
            agent.register_tools([{"name": "calculator"}], executor=MagicMock(return_value="2"))

            response = agent.chat("Keep calculating forever")

        assert "wasn't able to finish" in response


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
