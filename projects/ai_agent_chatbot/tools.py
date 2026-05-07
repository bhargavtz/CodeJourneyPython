"""
Tool definitions for the AI agent.

Provides tool schemas that the agent can use:
- calculator: Perform mathematical operations
- weather: Get weather information (simulated)
- search: Web search (simulated)

Author: CodeJourney AI Project
License: MIT
"""

import logging
from typing import Dict, Any, List
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class Tool(ABC):
    """Base class for tools."""

    @abstractmethod
    def get_schema(self) -> Dict[str, Any]:
        """Get tool schema for Claude API."""
        pass

    @abstractmethod
    def execute(self, **kwargs) -> str:
        """Execute tool with given inputs."""
        pass


class CalculatorTool(Tool):
    """Tool for performing mathematical calculations."""

    def get_schema(self) -> Dict[str, Any]:
        """Get schema for calculator tool."""
        return {
            "name": "calculator",
            "description": (
                "Perform mathematical calculations. Supports basic arithmetic, "
                "trigonometry, logarithms, and more."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to evaluate (e.g., '15 * 27 + 42')",
                    },
                    "precision": {
                        "type": "integer",
                        "description": "Decimal places for result (default: 2)",
                        "default": 2,
                    }
                },
                "required": ["expression"],
            },
        }

    def execute(self, expression: str, precision: int = 2) -> str:
        """
        Execute mathematical expression.

        Args:
            expression: Math expression to evaluate
            precision: Decimal places for result

        Returns:
            Calculation result as string
        """
        try:
            # Use eval with restricted namespace for safety
            allowed_names = {
                "abs": abs, "round": round, "min": min, "max": max,
                "pow": pow, "sum": sum
            }
            # Add common math functions
            import math
            allowed_names.update({
                name: getattr(math, name)
                for name in dir(math)
                if not name.startswith("_")
            })

            result = eval(expression, {"__builtins__": {}}, allowed_names)
            result = round(result, precision)
            logger.info(f"Calculator: {expression} = {result}")
            return f"{expression} = {result}"

        except ZeroDivisionError:
            logger.warning(f"Division by zero in: {expression}")
            return "Error: Division by zero"
        except Exception as e:
            logger.error(f"Calculation error: {e}")
            return f"Error: Invalid expression - {str(e)}"


class WeatherTool(Tool):
    """Tool for getting weather information (simulated)."""

    def get_schema(self) -> Dict[str, Any]:
        """Get schema for weather tool."""
        return {
            "name": "get_weather",
            "description": (
                "Get current weather conditions for a specified location. "
                "Returns temperature, conditions, and forecast."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name or geographic location",
                    },
                    "units": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "Temperature units (default: celsius)",
                        "default": "celsius",
                    }
                },
                "required": ["location"],
            },
        }

    def execute(self, location: str, units: str = "celsius") -> str:
        """
        Get weather for location (simulated).

        Args:
            location: City or location name
            units: Temperature units

        Returns:
            Weather information as string
        """
        # In production, this would call a real weather API
        weather_data = {
            "New York": ("15°C", "Cloudy"),
            "London": ("12°C", "Rainy"),
            "Tokyo": ("22°C", "Sunny"),
            "Sydney": ("25°C", "Clear"),
        }

        if location in weather_data:
            temp, condition = weather_data[location]
            logger.info(f"Weather lookup: {location}")
            return f"Weather in {location}: {temp}, {condition}"
        else:
            logger.warning(f"Weather data not available for: {location}")
            return f"Sorry, I don't have weather data for {location}"


class SearchTool(Tool):
    """Tool for web search (simulated)."""

    def get_schema(self) -> Dict[str, Any]:
        """Get schema for search tool."""
        return {
            "name": "search",
            "description": (
                "Search the web for information about a topic. "
                "Returns relevant results and snippets."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query",
                    },
                    "num_results": {
                        "type": "integer",
                        "description": "Number of results to return (1-10, default: 3)",
                        "default": 3,
                    }
                },
                "required": ["query"],
            },
        }

    def execute(self, query: str, num_results: int = 3) -> str:
        """
        Search for information (simulated).

        Args:
            query: Search query
            num_results: Number of results to return

        Returns:
            Search results as string
        """
        # In production, this would call a real search API
        logger.info(f"Search query: {query}")
        return (
            f"Search Results for '{query}':\n"
            f"1. Result about {query} - This is a simulated search result\n"
            f"2. More information about {query} - Additional context here\n"
            f"3. Related to {query} - More relevant information"
        )


def get_all_tools() -> List[Dict[str, Any]]:
    """
    Get all available tool schemas.

    Returns:
        List of tool definitions for Claude API
    """
    tools = [
        CalculatorTool(),
        WeatherTool(),
        SearchTool(),
    ]
    return [tool.get_schema() for tool in tools]


def execute_tool(tool_name: str, **kwargs) -> str:
    """
    Execute a tool by name.

    Args:
        tool_name: Name of tool to execute
        **kwargs: Arguments for the tool

    Returns:
        Tool execution result

    Raises:
        ValueError: If tool not found
    """
    tools_map = {
        "calculator": CalculatorTool(),
        "get_weather": WeatherTool(),
        "search": SearchTool(),
    }

    if tool_name not in tools_map:
        raise ValueError(f"Unknown tool: {tool_name}")

    tool = tools_map[tool_name]
    return tool.execute(**kwargs)
