"""Offline tests for the from-scratch model-coding lesson."""
from unittest.mock import patch

import pytest

from projects.ai_agents.model_coding_from_scratch.client import ModelAPIError
from projects.ai_agents.model_coding_from_scratch.main import (
    classify_support_message,
    conversation,
)


class TestConversation:
    @patch("projects.ai_agents.model_coding_from_scratch.main.chat")
    def test_history_is_resend_and_assistant_reply_is_appended(self, mock_chat):
        mock_chat.return_value = ("Hello Bhargav!", {"total_tokens": 10})
        answer, history = conversation("What is my name?", [{"role": "user", "content": "My name is Bhargav."}])
        assert answer == "Hello Bhargav!"
        assert history[-1] == {"role": "assistant", "content": "Hello Bhargav!"}
        assert mock_chat.call_args.args[0][0]["content"] == "My name is Bhargav."


class TestStructuredClassification:
    @patch("projects.ai_agents.model_coding_from_scratch.main.chat")
    def test_valid_json_is_parsed_and_validated(self, mock_chat):
        mock_chat.return_value = (
            '{"category":"billing","urgency":"high","summary":"Duplicate charge needs refund"}',
            {},
        )
        result = classify_support_message("I was charged twice")
        assert result["category"] == "billing"
        assert result["urgency"] == "high"

    @patch("projects.ai_agents.model_coding_from_scratch.main.chat")
    def test_invalid_json_is_rejected(self, mock_chat):
        mock_chat.return_value = ("not json", {})
        with pytest.raises(ValueError, match="valid JSON"):
            classify_support_message("hello")

    @patch("projects.ai_agents.model_coding_from_scratch.main.chat")
    def test_unknown_category_is_rejected(self, mock_chat):
        mock_chat.return_value = (
            '{"category":"made_up","urgency":"low","summary":"x"}',
            {},
        )
        with pytest.raises(ValueError, match="category"):
            classify_support_message("hello")


class TestClientErrors:
    @patch("projects.ai_agents.model_coding_from_scratch.client.API_KEY", "")
    def test_missing_key_has_a_clear_error(self):
        from projects.ai_agents.model_coding_from_scratch.client import chat

        with pytest.raises(ModelAPIError, match="AI_API_KEY is missing"):
            chat([{"role": "user", "content": "hello"}])
