"""
Utility modules for CodeJourneyPython projects.

Provides common functionality for:
- Logging configuration
- Error handling patterns
- Data validation
- Configuration management
"""

from .errors import BaseProjectError, ConfigurationError, ValidationError
from .logging_config import get_logger, setup_logger

__all__ = [
    "setup_logger",
    "get_logger",
    "BaseProjectError",
    "ValidationError",
    "ConfigurationError",
]
