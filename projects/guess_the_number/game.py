"""
Guess the Number Game - A beginner-level interactive number guessing game.

This module implements a simple number guessing game where the player attempts
to guess a randomly generated number between 1-100. The game provides feedback
on each guess (too high, too low, or correct) and tracks the number of attempts.

Example:
    To run the game directly:

    >>> python game.py
    Welcome to 'Guess the Number'!
    I'm thinking of a number between 1 and 100.
    Enter your guess: 50
    Too high! Try again.
    ...

Learning Objectives:
    - Random number generation
    - User input handling and validation
    - Control flow (while loops, conditionals)
    - Exception handling (ValueError, KeyboardInterrupt)
    - Function definition and module structure
"""

import logging
import random
from typing import Optional

# Configure logging for the game
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


class InvalidGuessError(Exception):
    """Raised when user input is not a valid number in range."""

    pass


class GameError(Exception):
    """Base exception for game-related errors."""

    pass


def guess_the_number() -> None:
    """
    Play an interactive number guessing game.

    The game generates a random integer between 1 and 100, then prompts
    the user to guess it. After each guess, feedback is provided:
    'Too low', 'Too high', or 'Correct!'. The game continues until the
    player guesses correctly or interrupts with Ctrl+C.

    Returns:
        None: Displays all output to stdout.

    Raises:
        KeyboardInterrupt: When user presses Ctrl+C during gameplay.

    Game Constants:
        - MIN_NUMBER (int): Minimum possible number (1)
        - MAX_NUMBER (int): Maximum possible number (100)
    """
    # Game configuration constants
    MIN_NUMBER: int = 1
    MAX_NUMBER: int = 100

    try:
        logger.info(f"Game started. Secret number between {MIN_NUMBER}-{MAX_NUMBER}")

        # Generate a random number between 1 and 100
        number_to_guess: int = random.randint(MIN_NUMBER, MAX_NUMBER)
        attempts: int = 0
        guessed: bool = False

        print("Welcome to 'Guess the Number'!")
        print(f"I'm thinking of a number between {MIN_NUMBER} and {MAX_NUMBER}.")

        # Loop until the user guesses the number correctly
        while not guessed:
            try:
                # Get user's guess
                user_input: str = input("Enter your guess: ")
                user_guess: int = int(user_input)
                attempts += 1

                # Validate guess is within valid range
                if user_guess < MIN_NUMBER or user_guess > MAX_NUMBER:
                    logger.warning(
                        f"Out of range guess: {user_guess} "
                        f"(valid range: {MIN_NUMBER}-{MAX_NUMBER})"
                    )
                    print(
                        f"Please guess a number between {MIN_NUMBER} and {MAX_NUMBER}."
                    )
                    continue

                logger.debug(f"Attempt {attempts}: User guessed {user_guess}")

                # Provide feedback on the guess
                if user_guess < number_to_guess:
                    print("Too low! Try again.")
                elif user_guess > number_to_guess:
                    print("Too high! Try again.")
                else:
                    # Correct guess - game won
                    guessed = True
                    logger.info(f"Correct! User won in {attempts} attempts")
                    print(
                        f"Congratulations! You've guessed the number {number_to_guess} "
                        f"in {attempts} attempt{'s' if attempts != 1 else ''}."
                    )

            except ValueError:
                logger.warning(f"Invalid input received: {user_input}")
                print("Please enter a valid integer.")
            except KeyboardInterrupt:
                logger.info("Game interrupted by user (Ctrl+C)")
                print("\nGame interrupted by user. Thanks for playing!")
                break

    except GameError as e:
        logger.error(f"Game error: {str(e)}")
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    guess_the_number()
