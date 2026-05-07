"""
Guess the Number Game - Base Camp Project.

A beginner-level interactive game demonstrating fundamental Python concepts.

Exports:
    guess_the_number: Main game function
    InvalidGuessError: Exception for invalid guesses
    GameError: Base exception for game errors
"""

from .game import GameError, InvalidGuessError, guess_the_number

__all__ = ["guess_the_number", "InvalidGuessError", "GameError"]
__version__ = "0.1.0"
