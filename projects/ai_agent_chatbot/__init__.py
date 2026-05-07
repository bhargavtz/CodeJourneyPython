"""
AI Agent Chatbot - River Crossing Project.

Intelligent conversational agent with LLM integration and tool use.
"""

from .agent import AIAgent, ConversationState, Message
from .tools import get_all_tools, execute_tool
from .config import Config

__version__ = "0.1.0"
__author__ = "CodeJourney"
__all__ = ["AIAgent", "ConversationState", "Message", "Config", "get_all_tools", "execute_tool"]
