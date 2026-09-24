"""Offline tests for Executor — no LLM calls involved at all."""

from projects.ai_agents.agent5_planner_executor.executor import Executor
from projects.ai_agents.agent5_planner_executor.planner import Step


class TestExecutorTools:
    def test_note_echoes_text_and_records_scratchpad(self):
        executor = Executor()
        step = Step(description="Remember something", tool="note", tool_input="The sky is blue")

        result = executor.execute_step(step, 1)

        assert result == "The sky is blue"
        assert "Step 1" in executor.scratchpad[0]

    def test_calculator_evaluates_expression(self):
        executor = Executor()
        step = Step(description="Do math", tool="calculator", tool_input="6 * 7")

        result = executor.execute_step(step, 1)

        assert result == "42"

    def test_write_file_saves_to_output_dir(self, tmp_path):
        executor = Executor(output_dir=str(tmp_path))
        step = Step(description="Save it", tool="write_file", tool_input="hello world")

        result = executor.execute_step(step, 3)

        saved_file = tmp_path / "step_3.txt"
        assert saved_file.exists()
        assert saved_file.read_text() == "hello world"
        assert "step_3.txt" in result

    def test_unknown_tool_is_reported_not_raised(self):
        executor = Executor()
        step = Step(description="???", tool="teleport", tool_input="nowhere")

        result = executor.execute_step(step, 1)

        assert "unknown tool" in result

    def test_scratchpad_accumulates_across_steps(self):
        executor = Executor()
        executor.execute_step(Step("first", "note", "a"), 1)
        executor.execute_step(Step("second", "note", "b"), 2)

        assert len(executor.scratchpad) == 2
