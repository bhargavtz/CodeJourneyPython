"""
Custom exception classes for CodeJourneyPython projects.

Provides a hierarchy of exceptions for better error handling and
more specific error reporting across all projects.
"""


class BaseProjectError(Exception):
    """Base exception class for all CodeJourneyPython errors."""

    def __init__(self, message: str, error_code: str = "UNKNOWN"):
        """
        Initialize exception with message and error code.

        Args:
            message: Human-readable error message
            error_code: Machine-readable error identifier
        """
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

    def __str__(self) -> str:
        """Return formatted error message with code."""
        return f"[{self.error_code}] {self.message}"


class ValidationError(BaseProjectError):
    """Raised when data validation fails."""

    def __init__(self, message: str, field: str = "unknown"):
        """
        Initialize validation error.

        Args:
            message: Error description
            field: Field name that failed validation
        """
        self.field = field
        super().__init__(message, "VALIDATION_ERROR")


class ConfigurationError(BaseProjectError):
    """Raised when configuration is invalid or missing."""

    def __init__(self, message: str, config_key: str = "unknown"):
        """
        Initialize configuration error.

        Args:
            message: Error description
            config_key: Configuration key that caused the error
        """
        self.config_key = config_key
        super().__init__(message, "CONFIG_ERROR")


class GameError(BaseProjectError):
    """Base exception for game-related errors."""

    def __init__(self, message: str):
        """Initialize game error."""
        super().__init__(message, "GAME_ERROR")


class InvalidGuessError(GameError):
    """Raised when user provides an invalid guess."""

    def __init__(self, guess: str, min_val: int = 1, max_val: int = 100):
        """
        Initialize invalid guess error.

        Args:
            guess: The invalid guess value
            min_val: Minimum valid value
            max_val: Maximum valid value
        """
        self.guess = guess
        self.min_val = min_val
        self.max_val = max_val
        message = (
            f"Invalid guess '{guess}'. Please enter a number between "
            f"{min_val} and {max_val}."
        )
        super().__init__(message)


class DataError(BaseProjectError):
    """Raised when data processing or loading fails."""

    def __init__(self, message: str, data_source: str = "unknown"):
        """
        Initialize data error.

        Args:
            message: Error description
            data_source: Source of the data that failed
        """
        self.data_source = data_source
        super().__init__(message, "DATA_ERROR")


class PipelineError(BaseProjectError):
    """Raised when data pipeline operations fail."""

    def __init__(self, message: str, stage: str = "unknown"):
        """
        Initialize pipeline error.

        Args:
            message: Error description
            stage: Pipeline stage where error occurred (extract, transform, load)
        """
        self.stage = stage
        super().__init__(message, "PIPELINE_ERROR")
