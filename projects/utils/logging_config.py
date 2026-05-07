"""
Logging configuration utilities for CodeJourneyPython projects.

Provides consistent logging setup across all projects with:
- Configurable log levels
- File and console output
- Structured logging format
"""

import logging
import logging.handlers
from pathlib import Path
from typing import Optional

# Global logger instances cache
_loggers = {}


def setup_logger(
    name: str,
    level: str = "INFO",
    log_file: Optional[str] = None,
    log_format: Optional[str] = None,
) -> logging.Logger:
    """
    Configure and return a logger instance with consistent formatting.

    Args:
        name: Logger name (typically __name__)
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path for file logging
        log_format: Optional custom log format string

    Returns:
        Configured logging.Logger instance

    Example:
        >>> logger = setup_logger(__name__, level="DEBUG")
        >>> logger.info("Application started")
    """
    if name in _loggers:
        return _loggers[name]

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Default format
    if log_format is None:
        log_format = (
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

    formatter = logging.Formatter(log_format)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (if specified)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Cache the logger
    _loggers[name] = logger
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a previously configured logger instance.

    Args:
        name: Logger name

    Returns:
        Configured logging.Logger instance or new default logger

    Raises:
        Returns a default logger if not previously configured
    """
    if name in _loggers:
        return _loggers[name]
    # Return default logger if not configured
    return logging.getLogger(name)


def disable_logging(name: str) -> None:
    """Disable a logger by name."""
    logger = logging.getLogger(name)
    logger.disabled = True


def enable_logging(name: str) -> None:
    """Enable a logger by name."""
    logger = logging.getLogger(name)
    logger.disabled = False
