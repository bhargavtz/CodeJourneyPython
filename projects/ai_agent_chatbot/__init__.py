"""
AI Agent Chatbot - River Crossing Project.

Intelligent conversational agent with LLM integration and tool use.
"""

from .agent import AIAgent, ConversationState, Message
from .config import Config
from .tools import execute_tool, get_all_tools

__version__ = "0.1.0"
__author__ = "CodeJourney"
__all__ = ["AIAgent", "ConversationState", "Message", "Config", "get_all_tools", "execute_tool"]
