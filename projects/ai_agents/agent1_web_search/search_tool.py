"""
Web search tool used by the Web Search Agent.

Wraps a DuckDuckGo search backend (no API key required) behind a small typed
interface, plus the JSON-schema the model uses to decide when to call it.
"""

import logging
from dataclasses import dataclass
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class SearchError(Exception):
    """Raised when no search backend is installed or the search fails."""


@dataclass
class SearchResult:
    """A single web search result."""

    title: str
    url: str
    snippet: str

    def to_dict(self) -> Dict[str, str]:
        """Return the result as a plain dict (JSON-serializable)."""
        return {"title": self.title, "url": self.url, "snippet": self.snippet}


def _load_ddgs_client() -> Any:
    """Import whichever DuckDuckGo search client is installed.

    The PyPI package behind this API was renamed from ``duckduckgo-search``
    to ``ddgs``; supporting both keeps the example working either way.
    """
    try:
        from ddgs import DDGS

        return DDGS
    except ImportError:
        pass

    try:
        from duckduckgo_search import DDGS

        return DDGS
    except ImportError as exc:
        raise SearchError(
            "No search backend installed. Run `pip install ddgs` and try again."
        ) from exc


def web_search(query: str, max_results: int = 5) -> List[SearchResult]:
    """Search the web via DuckDuckGo and return the top results.

    Args:
        query: The search query text.
        max_results: Maximum number of results to return.

    Returns:
        A list of SearchResult objects (empty if nothing was found).

    Raises:
        SearchError: If no search backend is installed, or the query fails.
    """
    ddgs_client = _load_ddgs_client()
    logger.info("Searching web for: %s", query)

    try:
        with ddgs_client() as ddgs:
            hits = list(ddgs.text(query, max_results=max_results))
    except SearchError:
        raise
    except Exception as exc:  # network/backend errors from the search library
        raise SearchError(f"Web search failed: {exc}") from exc

    results = [
        SearchResult(
            title=hit.get("title", ""),
            url=hit.get("href") or hit.get("url", ""),
            snippet=hit.get("body", ""),
        )
        for hit in hits
    ]
    logger.info("Found %d results", len(results))
    return results


TOOL_SCHEMA: Dict[str, Any] = {
    "name": "web_search",
    "description": (
        "Search the public web for up-to-date information. Use this whenever "
        "a question depends on facts you are not fully confident about, or "
        "anything time-sensitive (news, prices, releases, current events)."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query to run.",
            },
            "max_results": {
                "type": "integer",
                "description": "Number of results to fetch (default 5).",
                "default": 5,
            },
        },
        "required": ["query"],
    },
}
