"""
Local tools for the ReAct agent.

Unlike Agent 1, these are not registered through the API's ``tools=``
parameter — the model is simply told (in the prompt) which tool names exist
and how to call them, and this module supplies the implementation the agent
loop dispatches to after parsing the model's plain-text output.
"""

import logging
import math
from typing import Dict

logger = logging.getLogger(__name__)

# A tiny, offline "knowledge base" so the demo works without any external API.
_KNOWLEDGE_BASE: Dict[str, str] = {
    "capital of france": "Paris",
    "capital of japan": "Tokyo",
    "speed of light": "299,792,458 m/s",
    "python creator": "Guido van Rossum",
}


class ToolExecutionError(Exception):
    """Raised when a tool cannot execute the given input."""


def calculator(expression: str) -> str:
    """Safely evaluate an arithmetic expression.

    Args:
        expression: A math expression, e.g. "15 * 27 + 42".

    Returns:
        The result formatted as a string.

    Raises:
        ToolExecutionError: If the expression is invalid or unsafe.
    """
    allowed_names = {name: getattr(math, name) for name in dir(math) if not name.startswith("_")}
    allowed_names.update({"abs": abs, "round": round, "min": min, "max": max, "pow": pow})

    try:
        result = eval(expression, {"__builtins__": {}}, allowed_names)  # noqa: S307
    except ZeroDivisionError as exc:
        raise ToolExecutionError("Division by zero.") from exc
    except Exception as exc:
        raise ToolExecutionError(f"Could not evaluate '{expression}': {exc}") from exc

    logger.info("calculator(%s) = %s", expression, result)
    return str(result)


def knowledge_lookup(topic: str) -> str:
    """Look up a fact in the small local knowledge base.

    Args:
        topic: A lowercase-insensitive topic key, e.g. "capital of france".

    Returns:
        The known fact, or a "not found" message the agent can react to.
    """
    answer = _KNOWLEDGE_BASE.get(topic.strip().lower())
    logger.info("knowledge_lookup(%s) -> %s", topic, answer)
    if answer is None:
        return f"No local knowledge for '{topic}'."
    return answer


TOOLS = {
    "calculator": calculator,
    "knowledge_lookup": knowledge_lookup,
}

# Rendered into the system prompt so the model knows what it can call and how.
TOOL_DESCRIPTIONS = """\
- calculator[expression]: evaluate an arithmetic expression, e.g. calculator[12 * 8]
- knowledge_lookup[topic]: look up a fact from a small local knowledge base, \
e.g. knowledge_lookup[capital of france]\
"""
