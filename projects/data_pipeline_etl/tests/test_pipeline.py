"""Unit tests for projects.data_pipeline_etl.pipeline."""

import pandas as pd
import pytest

from projects.data_pipeline_etl.pipeline import Pipeline, PipelineStatistics, PipelineStatus


class _StubPipeline(Pipeline):
    """A minimal concrete Pipeline for testing the base class's orchestration."""

    def __init__(self, name="Stub Pipeline", fail_at=None):
        super().__init__(name)
        self.fail_at = fail_at

    def extract(self) -> pd.DataFrame:
        if self.fail_at == "extract":
            raise ValueError("extract failed")
        return pd.DataFrame({"a": [1, 2, 3]})

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.fail_at == "transform":
            raise ValueError("transform failed")
        return df.assign(b=df["a"] * 2)

    def load(self, df: pd.DataFrame) -> None:
        if self.fail_at == "load":
            raise ValueError("load failed")
        self.loaded_df = df


class TestPipelineBaseClass:
    def test_extract_transform_load_are_not_implemented(self):
        pipeline = Pipeline("Bare Pipeline")
        with pytest.raises(NotImplementedError):
            pipeline.extract()
        with pytest.raises(NotImplementedError):
            pipeline.transform(pd.DataFrame())
        with pytest.raises(NotImplementedError):
            pipeline.load(pd.DataFrame())


class TestPipelineRun:
    def test_full_run_succeeds_and_updates_stats(self):
        pipeline = _StubPipeline()

        success = pipeline.run()

        assert success is True
        assert pipeline.status == PipelineStatus.SUCCESS
        assert pipeline.stats.rows_extracted == 3
        assert pipeline.stats.rows_transformed == 3
        assert pipeline.stats.rows_loaded == 3
        assert pipeline.loaded_df["b"].tolist() == [2, 4, 6]

    def test_single_stage_run(self):
        pipeline = _StubPipeline()

        success = pipeline.run(stage="extract")

        assert success is True
        assert pipeline.data is not None
        assert pipeline.stats.rows_transformed == 0  # transform never ran

    def test_transform_without_prior_extract_fails(self):
        pipeline = _StubPipeline()

        success = pipeline.run(stage="transform")

        assert success is False
        assert pipeline.status == PipelineStatus.FAILED

    def test_run_applies_registered_transformations(self):
        pipeline = _StubPipeline()
        pipeline.add_transformation(lambda df: df.assign(c=df["a"] + 100))

        pipeline.run()

        assert pipeline.loaded_df["c"].tolist() == [101, 102, 103]

    def test_failure_in_a_stage_marks_pipeline_failed(self):
        pipeline = _StubPipeline(fail_at="transform")

        success = pipeline.run()

        assert success is False
        assert pipeline.status == PipelineStatus.FAILED
        assert len(pipeline.stats.errors) == 1


class TestPipelineValidateData:
    def test_valid_data_passes(self):
        pipeline = _StubPipeline()
        df = pd.DataFrame({"age": [10, 20, 30]})
        assert pipeline.validate_data(df, rules={"age": lambda s: (s >= 0).all()}) is True

    def test_missing_column_raises(self):
        pipeline = _StubPipeline()
        df = pd.DataFrame({"age": [10]})
        with pytest.raises(ValueError):
            pipeline.validate_data(df, rules={"missing": lambda s: True})

    def test_failing_rule_raises(self):
        pipeline = _StubPipeline()
        df = pd.DataFrame({"age": [-5]})
        with pytest.raises(ValueError):
            pipeline.validate_data(df, rules={"age": lambda s: (s >= 0).all()})


class TestPipelineHandleError:
    def test_log_action_records_but_does_not_raise(self):
        pipeline = _StubPipeline()
        pipeline.handle_error(ValueError("oops"), action="log")
        assert len(pipeline.stats.errors) == 1

    def test_raise_action_reraises(self):
        pipeline = _StubPipeline()
        with pytest.raises(ValueError):
            pipeline.handle_error(ValueError("oops"), action="raise")

    def test_skip_action_records_but_does_not_raise(self):
        pipeline = _StubPipeline()
        pipeline.handle_error(ValueError("oops"), action="skip")
        assert len(pipeline.stats.errors) == 1


class TestPipelineGetStatus:
    def test_status_reflects_a_successful_run(self):
        pipeline = _StubPipeline()
        pipeline.run()
        status = pipeline.get_status()
        assert status["success"] is True
        assert status["rows_loaded"] == 3


class TestPipelineStatistics:
    def test_success_rate_is_zero_with_no_rows_extracted(self):
        stats = PipelineStatistics()
        assert stats.success_rate == 0.0

    def test_success_rate_reflects_loaded_over_extracted(self):
        stats = PipelineStatistics(rows_extracted=10, rows_loaded=5)
        assert stats.success_rate == 50.0

    def test_get_status_without_errors_is_success(self):
        stats = PipelineStatistics(rows_loaded=1)
        assert stats.get_status() == "SUCCESS"

    def test_get_status_with_errors_but_some_rows_is_partial_failure(self):
        stats = PipelineStatistics(rows_loaded=1, errors=["boom"])
        assert stats.get_status() == "PARTIAL_FAILURE"

    def test_get_status_with_errors_and_no_rows_is_failed(self):
        stats = PipelineStatistics(rows_loaded=0, errors=["boom"])
        assert stats.get_status() == "FAILED"
