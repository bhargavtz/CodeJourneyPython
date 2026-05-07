#!/usr/bin/env python3
"""
AI Agent Chatbot CLI - Interactive conversation interface.

Run this script to start an interactive chat session with the AI agent.

Usage:
    python main.py                  # Start interactive mode
    python main.py --help          # Show help message
    python main.py --debug         # Run with debug logging

Author: CodeJourney AI Project
License: MIT
"""

import os
import sys
import logging
import argparse
from pathlib import Path
from dotenv import load_dotenv

from agent import AIAgent
from tools import get_all_tools, execute_tool
from config import Config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


class ChatbotCLI:
    """Interactive CLI for the AI Agent."""

    COMMANDS = {
        "exit": "Exit the chatbot",
        "quit": "Exit the chatbot",
        "clear": "Clear conversation history",
        "help": "Show this help message",
        "stats": "Show conversation statistics",
        "save": "Save conversation to file",
        "load": "Load conversation from file",
        "system": "Set system prompt",
    }

    def __init__(self, agent: AIAgent):
        """
        Initialize CLI.

        Args:
            agent: AI Agent instance
        """
        self.agent = agent
        self.running = True

    def print_welcome(self) -> None:
        """Print welcome message."""
        print("\n" + "=" * 60)
        print("🤖 AI Agent Chatbot - River Crossing")
        print("=" * 60)
        print("Type 'help' for commands, 'exit' to quit\n")

    def print_help(self) -> None:
        """Print available commands."""
        print("\nAvailable Commands:")
        for cmd, desc in self.COMMANDS.items():
            print(f"  {cmd:<15} - {desc}")
        print()

    def handle_command(self, user_input: str) -> bool:
        """
        Handle special commands.

        Args:
            user_input: User input text

        Returns:
            False if should exit, True to continue
        """
        command = user_input.lower().strip()

        if command in ["exit", "quit"]:
            print("\nGoodbye! 👋\n")
            return False

        elif command == "clear":
            self.agent.clear_conversation()
            print("✓ Conversation cleared\n")

        elif command == "help":
            self.print_help()

        elif command == "stats":
            print("\n" + self.agent.get_statistics() + "\n")

        elif command.startswith("save "):
            filepath = command[5:].strip()
            self.agent.save_conversation(filepath)
            print(f"✓ Saved to {filepath}\n")

        elif command.startswith("load "):
            filepath = command[5:].strip()
            self.agent.load_conversation(filepath)
            print(f"✓ Loaded from {filepath}\n")

        elif command.startswith("system "):
            new_prompt = command[7:].strip()
            self.agent.set_system_prompt(new_prompt)
            print("✓ System prompt updated\n")

        elif command:
            return None  # Not a command, treat as regular message

        return True

    def run(self) -> None:
        """Run the interactive CLI loop."""
        self.print_welcome()

        while self.running:
            try:
                # Get user input
                user_input = input("You: ").strip()

                if not user_input:
                    continue

                # Check if it's a command
                result = self.handle_command(user_input)
                if result is False:
                    break
                elif result is True:
                    continue

                # Get agent response
                print("\nAgent: ", end="", flush=True)
                response = self.agent.chat(user_input)
                print(response + "\n")

            except KeyboardInterrupt:
                print("\n\nInterrupted. Type 'exit' to quit.\n")
            except EOFError:
                print("\nGoodbye! 👋\n")
                break
            except Exception as e:
                logger.error(f"Error in chat loop: {e}")
                print(f"Error: {str(e)}\n")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="AI Agent Chatbot - Interactive conversation interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Start interactive mode
  python main.py --debug            # Run with debug logging
  python main.py --model gpt-4      # Use different model
        """
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )
    parser.add_argument(
        "--model",
        default="claude-opus-4-7",
        help="Claude model to use (default: claude-opus-4-7)"
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=2048,
        help="Maximum tokens per response (default: 2048)"
    )
    parser.add_argument(
        "--system-prompt",
        help="Custom system prompt"
    )

    args = parser.parse_args()

    # Setup logging
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")

    # Load environment variables
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        print("Please create a .env file with: ANTHROPIC_API_KEY=your-key")
        sys.exit(1)

    try:
        # Initialize agent
        logger.info("Initializing AI Agent...")
        agent = AIAgent(
            api_key=api_key,
            model=args.model,
            max_tokens=args.max_tokens,
            system_prompt=args.system_prompt
        )

        # Register tools
        tools = get_all_tools()
        agent.register_tools(tools)
        logger.info(f"Registered {len(tools)} tools")

        # Run CLI
        cli = ChatbotCLI(agent)
        cli.run()

    except ValueError as e:
        print(f"Configuration Error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
