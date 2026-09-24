"""
AI Agent implementation using Claude API with tool use capability.

This module implements an intelligent conversational agent that can:
- Maintain conversation history across multiple turns
- Use external tools (calculator, web search, etc.)
- Handle tool responses and incorporate them into responses
- Manage API interactions with error handling

Author: CodeJourney AI Project
License: MIT
"""

import json
import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from anthropic import Anthropic, APIError, RateLimitError

logger = logging.getLogger(__name__)

MAX_TOOL_ROUNDS = 5


@dataclass
class Message:
    """Represents a single conversation message."""

    role: str  # "user" or "assistant"
    content: str
    tokens: int = 0

    def to_dict(self) -> Dict[str, str]:
        """Convert message to API format."""
        return {"role": self.role, "content": self.content}


@dataclass
class ToolUse:
    """Represents a tool use request from the model."""

    name: str
    input: Dict[str, Any]
    id: str = ""


@dataclass
class ConversationState:
    """Manages conversation state and statistics."""

    messages: List[Message] = field(default_factory=list)
    total_tokens: int = 0
    tool_uses: int = 0
    errors: int = 0

    def add_message(self, role: str, content: str, tokens: int = 0) -> None:
        """Add message to conversation history."""
        self.messages.append(Message(role, content, tokens))
        self.total_tokens += tokens

    def clear(self) -> None:
        """Clear conversation history."""
        self.messages.clear()
        self.total_tokens = 0
        self.tool_uses = 0
        self.errors = 0

    def get_history(self) -> List[Dict[str, str]]:
        """Get conversation history in API format."""
        return [msg.to_dict() for msg in self.messages]

    def summary(self) -> str:
        """Get conversation statistics summary."""
        return (
            f"Conversation Summary:\n"
            f"  Messages: {len(self.messages)}\n"
            f"  Total Tokens: {self.total_tokens}\n"
            f"  Tool Uses: {self.tool_uses}\n"
            f"  Errors: {self.errors}"
        )


class AIAgent:
    """
    Intelligent agent powered by Claude API.

    Handles conversation management, tool use, and API interactions.

    Attributes:
        model: Claude model to use
        max_tokens: Maximum tokens per response
        state: Conversation state tracker
    """

    def __init__(
        self,
        api_key: str,
        model: str = "claude-opus-4-7",
        max_tokens: int = 2048,
        system_prompt: Optional[str] = None,
    ):
        """
        Initialize the AI agent.

        Args:
            api_key: Anthropic API key
            model: Claude model identifier (default: claude-opus-4-7)
            max_tokens: Maximum tokens per response (default: 2048)
            system_prompt: Optional system prompt to customize behavior

        Raises:
            ValueError: If API key is empty
        """
        if not api_key:
            raise ValueError("API key cannot be empty")

        self.client = Anthropic(api_key=api_key)
        self.model = model
        self.max_tokens = max_tokens
        self.system_prompt = system_prompt or self._get_default_system_prompt()
        self.state = ConversationState()
        self.tools: List[Dict[str, Any]] = []
        self.tool_executor: Optional[Callable[..., str]] = None

        logger.info(f"Initialized AI Agent with model: {model}")

    def _get_default_system_prompt(self) -> str:
        """Get default system prompt."""
        return (
            "You are a helpful AI assistant. You have access to tools that can "
            "help you provide better answers. Use tools when necessary to get "
            "accurate information or perform calculations. Always be honest about "
            "your capabilities and limitations."
        )

    def register_tools(
        self,
        tools: List[Dict[str, Any]],
        executor: Optional[Callable[..., str]] = None,
    ) -> None:
        """
        Register available tools.

        Args:
            tools: List of tool definitions in Claude API format
            executor: Callable that runs a tool by name, e.g.
                ``executor(tool_name, **tool_input) -> str``. Required for the
                agent to actually execute a tool the model asks for; without
                it, tool_use requests are reported back to the model as errors.
        """
        self.tools = tools
        self.tool_executor = executor
        logger.info(f"Registered {len(tools)} tools")

    def chat(self, user_message: str) -> str:
        """
        Send a message to the agent and get a response.

        Handles tool use internally and returns final response text.

        Args:
            user_message: The user's input message

        Returns:
            The agent's response text

        Raises:
            APIError: If API call fails after retries
        """
        logger.info(f"User: {user_message}")

        # Add user message to history
        self.state.add_message("user", user_message)

        try:
            final_response = self._run_tool_loop()

            # Add assistant response to history
            self.state.add_message("assistant", final_response)

            logger.info(f"Agent: {final_response[:100]}...")
            return final_response

        except RateLimitError:
            error_msg = "I'm currently rate limited. Please try again in a moment."
            self.state.errors += 1
            logger.error("Rate limit exceeded")
            return error_msg

        except APIError as e:
            error_msg = f"API Error: {str(e)[:100]}"
            self.state.errors += 1
            logger.error(f"API Error: {e}")
            return error_msg

        except Exception as e:
            error_msg = f"Unexpected error: {str(e)[:100]}"
            self.state.errors += 1
            logger.error(f"Unexpected error: {e}")
            return error_msg

    def _run_tool_loop(self) -> str:
        """
        Call Claude, executing any tools it requests, until it answers directly.

        Starts from the persisted conversation history and extends it with a
        transient sequence of assistant/tool_result turns local to this call
        (the flat, plain-text ``ConversationState`` only ever records the
        final answer, matching what a chat UI would actually display).

        Returns:
            The agent's final response text.
        """
        messages: List[Dict[str, Any]] = self.state.get_history()

        for _ in range(MAX_TOOL_ROUNDS):
            response = self._call_claude(messages)

            text_parts: List[str] = []
            tool_use_blocks: List[Any] = []
            for block in response.content:
                if getattr(block, "type", None) == "tool_use":
                    tool_use_blocks.append(block)
                else:
                    text_parts.append(getattr(block, "text", ""))

            if not tool_use_blocks:
                return "".join(text_parts) or "I couldn't generate a response. Please try again."

            messages.append({"role": "assistant", "content": response.content})

            tool_results = []
            for block in tool_use_blocks:
                self.state.tool_uses += 1
                result = self._execute_tool(block)
                tool_results.append(
                    {"type": "tool_result", "tool_use_id": block.id, "content": result}
                )
            messages.append({"role": "user", "content": tool_results})

        return "I wasn't able to finish using tools to answer that. Please try rephrasing."

    def _execute_tool(self, block: Any) -> str:
        """
        Run a single tool_use block via the registered executor.

        Args:
            block: A tool_use content block from a Claude response.

        Returns:
            The tool's result as a string, or a descriptive error message.
        """
        logger.debug(f"Tool use detected: {block.name}")

        if self.tool_executor is None:
            return f"Error: no tool executor registered for '{block.name}'"

        try:
            return str(self.tool_executor(block.name, **block.input))
        except Exception as e:
            logger.error(f"Tool execution failed for {block.name}: {e}")
            return f"Error executing tool '{block.name}': {e}"

    def _call_claude(self, messages: List[Dict[str, Any]]) -> Any:
        """
        Call Claude API with the given message history.

        Args:
            messages: Conversation history in API format.

        Returns:
            API response object
        """
        request_kwargs: Dict[str, Any] = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "system": self.system_prompt,
            "messages": messages,
        }

        # Add tools if registered
        if self.tools:
            request_kwargs["tools"] = self.tools

        logger.debug(f"Calling Claude API with {len(messages)} messages")
        return self.client.messages.create(**request_kwargs)

    def clear_conversation(self) -> None:
        """Clear conversation history and reset state."""
        self.state.clear()
        logger.info("Conversation cleared")

    def get_conversation_history(self) -> List[Dict[str, str]]:
        """
        Get current conversation history.

        Returns:
            List of messages in API format
        """
        return self.state.get_history()

    def get_statistics(self) -> str:
        """
        Get conversation statistics.

        Returns:
            Human-readable statistics summary
        """
        return self.state.summary()

    def set_system_prompt(self, prompt: str) -> None:
        """
        Update system prompt (affects subsequent messages).

        Args:
            prompt: New system prompt
        """
        self.system_prompt = prompt
        logger.info("System prompt updated")

    def save_conversation(self, filepath: str) -> None:
        """
        Save conversation to JSON file.

        Args:
            filepath: Path to save conversation
        """
        data = {
            "model": self.model,
            "messages": self.state.get_history(),
            "statistics": {
                "total_messages": len(self.state.messages),
                "total_tokens": self.state.total_tokens,
                "errors": self.state.errors,
            },
        }

        try:
            with open(filepath, "w") as f:
                json.dump(data, f, indent=2)
            logger.info(f"Conversation saved to {filepath}")
        except IOError as e:
            logger.error(f"Failed to save conversation: {e}")

    def load_conversation(self, filepath: str) -> None:
        """
        Load conversation from JSON file.

        Args:
            filepath: Path to load conversation from
        """
        try:
            with open(filepath, "r") as f:
                data = json.load(f)

            self.state.clear()
            for msg in data.get("messages", []):
                self.state.add_message(msg["role"], msg["content"])

            logger.info(f"Conversation loaded from {filepath}")
        except IOError as e:
            logger.error(f"Failed to load conversation: {e}")
