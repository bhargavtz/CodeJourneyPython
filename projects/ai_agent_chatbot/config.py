"""
Configuration management for the AI Agent Chatbot.

Handles loading configuration from environment variables and config files.

Author: CodeJourney AI Project
License: MIT
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    """Configuration settings for AI Agent."""

    # API Settings
    api_key: str = ""
    model: str = "claude-opus-4-7"
    max_tokens: int = 2048

    # Agent Settings
    system_prompt: Optional[str] = None
    temperature: float = 0.7
    timeout: int = 30

    # Tool Settings
    enable_calculator: bool = True
    enable_weather: bool = True
    enable_search: bool = True

    # Logging Settings
    debug_mode: bool = False
    log_file: Optional[str] = None

    # Storage Settings
    save_conversations: bool = True
    conversation_dir: str = "./conversations"

    @classmethod
    def from_env(cls) -> "Config":
        """
        Load configuration from environment variables.

        Returns:
            Config instance with values from environment
        """
        return cls(
            api_key=os.getenv("ANTHROPIC_API_KEY", ""),
            model=os.getenv("AI_MODEL", "claude-opus-4-7"),
            max_tokens=int(os.getenv("AI_MAX_TOKENS", "2048")),
            temperature=float(os.getenv("AI_TEMPERATURE", "0.7")),
            timeout=int(os.getenv("AI_TIMEOUT", "30")),
            debug_mode=os.getenv("DEBUG", "").lower() in ("true", "1", "yes"),
            save_conversations=os.getenv("SAVE_CONVERSATIONS", "true").lower() in ("true", "1", "yes"),
        )

    def validate(self) -> bool:
        """
        Validate configuration.

        Returns:
            True if valid, raises ValueError otherwise
        """
        if not self.api_key:
            raise ValueError("API key is required")
        if self.max_tokens < 1:
            raise ValueError("max_tokens must be positive")
        if not 0 <= self.temperature <= 2:
            raise ValueError("temperature must be between 0 and 2")
        return True
