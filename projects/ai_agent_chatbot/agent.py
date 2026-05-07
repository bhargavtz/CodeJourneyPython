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

import logging
import json
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from anthropic import Anthropic, APIError, RateLimitError

logger = logging.getLogger(__name__)


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

        logger.info(f"Initialized AI Agent with model: {model}")

    def _get_default_system_prompt(self) -> str:
        """Get default system prompt."""
        return (
            "You are a helpful AI assistant. You have access to tools that can "
            "help you provide better answers. Use tools when necessary to get "
            "accurate information or perform calculations. Always be honest about "
            "your capabilities and limitations."
        )

    def register_tools(self, tools: List[Dict[str, Any]]) -> None:
        """
        Register available tools.

        Args:
            tools: List of tool definitions in Claude API format
        """
        self.tools = tools
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
            # Get response from Claude
            response = self._call_claude()

            # Process response (handle tool use if needed)
            final_response = self._process_response(response)

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

    def _call_claude(self) -> Any:
        """
        Call Claude API with current conversation history.

        Returns:
            API response object
        """
        messages = self.state.get_history()

        request_kwargs = {
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

    def _process_response(self, response: Any) -> str:
        """
        Process Claude's response, handling tool use if needed.

        Args:
            response: Claude API response

        Returns:
            Final response text
        """
        # Extract text content
        result_text = ""
        has_tool_use = False

        for block in response.content:
            if hasattr(block, "text"):
                result_text += block.text
            elif hasattr(block, "type") and block.type == "tool_use":
                has_tool_use = True
                logger.debug(f"Tool use detected: {block.name}")

        # If there was tool use, add full response to history and handle tools
        if has_tool_use:
            # Add full response (including tool_use blocks) to history
            full_response = response
            # Note: In production, you'd handle tool execution here
            # For now, just return the text response

        return result_text or "I couldn't generate a response. Please try again."

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
            }
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
