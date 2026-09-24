"""Offline tests for PlannerExecutorAgent's end-to-end orchestration."""

from unittest.mock import MagicMock, patch

import pytest

from projects.ai_agents.agent5_planner_executor.agent import AgentError, PlannerExecutorAgent
from projects.ai_agents.agent5_planner_executor.planner import Step


class TestPlannerExecutorAgentInit:
    def test_requires_api_key(self):
        with pytest.raises(AgentError):
            PlannerExecutorAgent(api_key="")


class TestPlannerExecutorAgentRun:
    def test_runs_plan_then_executes_then_summarizes(self, tmp_path):
        with patch("projects.ai_agents.agent5_planner_executor.agent.Anthropic"):
            agent = PlannerExecutorAgent(api_key="sk-test", output_dir=str(tmp_path))

        fake_plan = [
            Step(description="Compute tip", tool="calculator", tool_input="45.50 * 0.2"),
            Step(
                description="Save explanation", tool="write_file", tool_input="A 20% tip is $9.10"
            ),
        ]
        agent.planner.plan = MagicMock(return_value=fake_plan)
        agent._summarize = MagicMock(return_value="Computed the tip and saved an explanation.")

        result = agent.run("Explain a 20% tip on $45.50 and save it")

        assert result.plan == fake_plan
        assert result.step_results[0] == "9.100000000000001" or result.step_results[0].startswith(
            "9.1"
        )
        assert "step_2.txt" in result.step_results[1]
        assert result.summary == "Computed the tip and saved an explanation."
        agent.planner.plan.assert_called_once_with("Explain a 20% tip on $45.50 and save it")

    def test_summarize_sends_step_report_to_the_model(self, tmp_path):
        with patch("projects.ai_agents.agent5_planner_executor.agent.Anthropic") as mock_cls:
            client = MagicMock()
            block = MagicMock(type="text", text="All done.")
            client.messages.create.return_value = MagicMock(content=[block])
            mock_cls.return_value = client

            agent = PlannerExecutorAgent(api_key="sk-test", output_dir=str(tmp_path))
            summary = agent._summarize("test goal", [Step("do it", "note", "x")], ["x"])

        assert summary == "All done."
        sent_content = client.messages.create.call_args.kwargs["messages"][0]["content"]
        assert "test goal" in sent_content
