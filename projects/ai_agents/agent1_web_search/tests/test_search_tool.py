"""Offline tests for the web search tool (no network access required)."""

from unittest.mock import MagicMock, patch

import pytest

from projects.ai_agents.agent1_web_search.search_tool import (
    TOOL_SCHEMA,
    SearchError,
    SearchResult,
    web_search,
)


class TestSearchResult:
    """Test the SearchResult dataclass."""

    def test_to_dict(self):
        result = SearchResult(title="Python", url="https://python.org", snippet="Official site")
        assert result.to_dict() == {
            "title": "Python",
            "url": "https://python.org",
            "snippet": "Official site",
        }


class TestToolSchema:
    """Test the Claude tool-definition schema."""

    def test_schema_has_required_fields(self):
        assert TOOL_SCHEMA["name"] == "web_search"
        assert "query" in TOOL_SCHEMA["input_schema"]["properties"]
        assert TOOL_SCHEMA["input_schema"]["required"] == ["query"]


class TestWebSearch:
    """Test web_search() against a mocked DDGS backend."""

    def _mock_ddgs(self, hits):
        mock_ddgs_instance = MagicMock()
        mock_ddgs_instance.text.return_value = iter(hits)
        mock_ddgs_instance.__enter__.return_value = mock_ddgs_instance
        mock_ddgs_instance.__exit__.return_value = False

        mock_client_class = MagicMock(return_value=mock_ddgs_instance)
        return mock_client_class

    def test_web_search_returns_results(self):
        hits = [{"title": "Result 1", "href": "https://a.example", "body": "Snippet A"}]
        mock_client = self._mock_ddgs(hits)

        with patch(
            "projects.ai_agents.agent1_web_search.search_tool._load_ddgs_client",
            return_value=mock_client,
        ):
            results = web_search("python release notes", max_results=1)

        assert len(results) == 1
        assert results[0].title == "Result 1"
        assert results[0].url == "https://a.example"

    def test_web_search_raises_when_no_backend_installed(self):
        with patch(
            "projects.ai_agents.agent1_web_search.search_tool._load_ddgs_client",
            side_effect=SearchError("No search backend installed."),
        ):
            with pytest.raises(SearchError):
                web_search("anything")
