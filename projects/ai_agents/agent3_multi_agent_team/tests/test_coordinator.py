"""Offline tests for the Coordinator's orchestration loop."""

from unittest.mock import MagicMock, patch

import pytest

from projects.ai_agents.agent3_multi_agent_team.coordinator import Coordinator, CoordinatorError


class TestCoordinatorInit:
    def test_requires_api_key(self):
        with pytest.raises(CoordinatorError):
            Coordinator(api_key="")


class TestCoordinatorRun:
    def _make_coordinator(self):
        with patch("projects.ai_agents.agent3_multi_agent_team.coordinator.Anthropic"):
            return Coordinator(api_key="sk-test")

    def test_approves_on_first_round(self):
        coordinator = self._make_coordinator()
        coordinator.writer.draft = MagicMock(return_value="Great draft")
        coordinator.reviewer.review = MagicMock(
            return_value=MagicMock(approved=True, feedback=None)
        )

        result = coordinator.run("test topic")

        assert result.approved is True
        assert result.final_draft == "Great draft"
        assert len(result.rounds) == 1
        coordinator.writer.draft.assert_called_once_with("test topic", feedback=None)

    def test_revises_once_then_approves(self):
        coordinator = self._make_coordinator()
        coordinator.writer.draft = MagicMock(side_effect=["Draft v1", "Draft v2"])
        coordinator.reviewer.review = MagicMock(
            side_effect=[
                MagicMock(approved=False, feedback="Needs an example"),
                MagicMock(approved=True, feedback=None),
            ]
        )

        result = coordinator.run("test topic")

        assert result.approved is True
        assert result.final_draft == "Draft v2"
        assert len(result.rounds) == 2
        second_call_kwargs = coordinator.writer.draft.call_args_list[1].kwargs
        assert second_call_kwargs["feedback"] == "Needs an example"

    def test_returns_best_effort_after_max_rounds(self):
        coordinator = self._make_coordinator()
        coordinator.writer.draft = MagicMock(return_value="Never good enough")
        coordinator.reviewer.review = MagicMock(
            return_value=MagicMock(approved=False, feedback="Still not right")
        )

        result = coordinator.run("test topic")

        assert result.approved is False
        assert result.final_draft == "Never good enough"
        assert len(result.rounds) == 3  # MAX_ROUNDS, no exception raised
