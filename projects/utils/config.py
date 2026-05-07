"""
Configuration management utilities for CodeJourneyPython projects.

Provides:
- Environment variable loading
- Configuration validation
- Default configuration values
"""

import os
from typing import Any, Dict, Optional
from pathlib import Path
import json


class Config:
    """Configuration manager for CodeJourneyPython projects."""

    # Default configuration values
    DEFAULTS: Dict[str, Any] = {
        "DEBUG": False,
        "LOG_LEVEL": "INFO",
        "LOG_FILE": None,
        "PROJECT_NAME": "CodeJourneyPython",
    }

    def __init__(self, env_file: Optional[str] = None):
        """
        Initialize configuration manager.

        Args:
            env_file: Path to .env file to load
        """
        self._config: Dict[str, Any] = self.DEFAULTS.copy()
        if env_file and Path(env_file).exists():
            self._load_env_file(env_file)
        self._load_environment()

    def _load_env_file(self, env_file: str) -> None:
        """Load configuration from .env file."""
        try:
            with open(env_file) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        if "=" in line:
                            key, value = line.split("=", 1)
                            self._config[key.strip()] = value.strip()
        except IOError as e:
            print(f"Warning: Could not read {env_file}: {e}")

    def _load_environment(self) -> None:
        """Load configuration from environment variables."""
        for key in self.DEFAULTS:
            if key in os.environ:
                self._config[key] = os.environ[key]

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        return self._config.get(key, default)

    def __getitem__(self, key: str) -> Any:
        """Get configuration value using dictionary syntax."""
        if key not in self._config:
            raise KeyError(f"Configuration key '{key}' not found")
        return self._config[key]

    def to_dict(self) -> Dict[str, Any]:
        """Return configuration as dictionary."""
        return self._config.copy()

    def to_json(self) -> str:
        """Return configuration as JSON string."""
        return json.dumps(self._config, indent=2)
