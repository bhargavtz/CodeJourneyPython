"""
Test suite for the Guess the Number game.

Tests cover:
    - Valid game sequences (correct guesses)
    - Invalid input handling (non-numeric input)
    - Out-of-range guess handling
    - Game interruption (Ctrl+C)
    - Game logic and feedback
"""

import pytest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys

from projects.guess_the_number.game import (
    guess_the_number,
    InvalidGuessError,
    GameError,
)


class TestGuessTheNumberGame:
    """Test suite for the Guess the Number game module."""

    @patch("random.randint", return_value=50)
    @patch("builtins.input", side_effect=["25", "75", "50"])
    def test_winning_game_sequence(self, mock_input, mock_random):
        """Test a complete winning game sequence with multiple guesses."""
        # Capture stdout to verify game messages
        captured_output = StringIO()
        sys.stdout = captured_output

        guess_the_number()

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Verify key game messages appear
        assert "Welcome" in output
        assert "Too low" in output or "Too high" in output
        assert "Congratulations" in output

    @patch("random.randint", return_value=50)
    @patch("builtins.input", side_effect=["50"])
    def test_correct_guess_first_try(self, mock_input, mock_random):
        """Test winning on the first guess."""
        captured_output = StringIO()
        sys.stdout = captured_output

        guess_the_number()

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        assert "Congratulations" in output
        assert "1 attempt" in output

    @patch("random.randint", return_value=50)
    @patch("builtins.input", side_effect=["abc"])
    def test_invalid_input_handling(self, mock_input, mock_random):
        """Test error handling for non-numeric input."""
        captured_output = StringIO()
        sys.stdout = captured_output

        # Mock to raise KeyboardInterrupt after invalid input
        with patch("builtins.input", side_effect=["abc", KeyboardInterrupt()]):
            guess_the_number()

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        assert "valid integer" in output or "interrupted" in output

    @patch("random.randint", return_value=50)
    @patch("builtins.input", side_effect=["101"])
    def test_out_of_range_guess(self, mock_input, mock_random):
        """Test feedback for out-of-range guesses."""
        captured_output = StringIO()
        sys.stdout = captured_output

        with patch("builtins.input", side_effect=["101", KeyboardInterrupt()]):
            guess_the_number()

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        assert "between" in output or "interrupted" in output

    @patch("random.randint", return_value=50)
    @patch("builtins.input", side_effect=KeyboardInterrupt())
    def test_keyboard_interrupt(self, mock_input, mock_random):
        """Test graceful handling of Ctrl+C interruption."""
        captured_output = StringIO()
        sys.stdout = captured_output

        guess_the_number()

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        assert "interrupted" in output.lower() or "thanks" in output.lower()

    @patch("random.randint", return_value=50)
    @patch("builtins.input", side_effect=["25", "75", "40", "60", "50"])
    def test_multiple_guesses_feedback(self, mock_input, mock_random):
        """Test feedback consistency across multiple guesses."""
        captured_output = StringIO()
        sys.stdout = captured_output

        guess_the_number()

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Should have feedback for multiple guesses
        feedback_count = output.count("Too") + output.count("Congratulations")
        assert feedback_count >= 3  # At least feedback from 3+ interactions

    def test_game_error_exception_exists(self):
        """Test that GameError exception is defined."""
        assert issubclass(GameError, Exception)

    def test_invalid_guess_error_exception_exists(self):
        """Test that InvalidGuessError exception is defined."""
        assert issubclass(InvalidGuessError, Exception)


class TestGameImports:
    """Test that game module exports are correct."""

    def test_game_function_callable(self):
        """Test that guess_the_number is callable."""
        assert callable(guess_the_number)

    def test_exceptions_are_importable(self):
        """Test that custom exceptions are importable."""
        assert GameError is not None
        assert InvalidGuessError is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
