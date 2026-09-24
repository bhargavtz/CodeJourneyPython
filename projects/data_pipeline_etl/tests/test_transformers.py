"""Unit tests for projects.data_pipeline_etl.transformers."""

import numpy as np
import pandas as pd
import pytest

from projects.data_pipeline_etl.transformers import (
    DeduplicationTransformer,
    EnrichmentTransformer,
    FilterTransformer,
    MissingValueTransformer,
    NormalizationTransformer,
    PipelineTransformer,
    Transformer,
    TypeConversionTransformer,
    ValidationTransformer,
)


class TestTransformerBaseClass:
    def test_transform_is_not_implemented(self):
        with pytest.raises(NotImplementedError):
            Transformer().transform(pd.DataFrame())


class TestDeduplicationTransformer:
    def test_removes_exact_duplicate_rows(self):
        df = pd.DataFrame({"a": [1, 1, 2], "b": ["x", "x", "y"]})
        result = DeduplicationTransformer().transform(df)
        assert len(result) == 2

    def test_subset_controls_which_columns_count(self):
        df = pd.DataFrame({"a": [1, 1, 2], "b": ["x", "y", "z"]})
        result = DeduplicationTransformer().transform(df, subset=["a"])
        assert len(result) == 2


class TestMissingValueTransformer:
    def test_drop_strategy_removes_rows_with_nulls(self):
        df = pd.DataFrame({"a": [1, np.nan, 3]})
        result = MissingValueTransformer().transform(df, strategy="drop")
        assert len(result) == 2

    def test_mean_strategy_fills_numeric_columns(self):
        df = pd.DataFrame({"a": [1.0, np.nan, 3.0]})
        result = MissingValueTransformer().transform(df, strategy="mean")
        assert result["a"].isnull().sum() == 0
        assert result["a"].iloc[1] == pytest.approx(2.0)

    def test_forward_fill_strategy(self):
        df = pd.DataFrame({"a": [1.0, np.nan, np.nan]})
        result = MissingValueTransformer().transform(df, strategy="forward_fill")
        assert result["a"].tolist() == [1.0, 1.0, 1.0]

    def test_value_strategy_requires_fill_value(self):
        df = pd.DataFrame({"a": [1, np.nan]})
        with pytest.raises(ValueError):
            MissingValueTransformer().transform(df, strategy="value")

    def test_value_strategy_fills_with_given_value(self):
        df = pd.DataFrame({"a": ["x", None]})
        result = MissingValueTransformer().transform(df, strategy="value", fill_value="unknown")
        assert result["a"].iloc[1] == "unknown"


class TestTypeConversionTransformer:
    def test_converts_column_to_target_type(self):
        df = pd.DataFrame({"age": ["30", "25"]})
        result = TypeConversionTransformer().transform(df, conversions={"age": "int64"})
        assert result["age"].dtype == np.int64

    def test_converts_to_datetime(self):
        df = pd.DataFrame({"date": ["2024-01-01", "2024-01-02"]})
        result = TypeConversionTransformer().transform(df, conversions={"date": "datetime"})
        assert pd.api.types.is_datetime64_any_dtype(result["date"])

    def test_missing_column_is_skipped_without_raising(self):
        df = pd.DataFrame({"a": [1, 2]})
        result = TypeConversionTransformer().transform(df, conversions={"missing": "int64"})
        assert list(result.columns) == ["a"]


class TestValidationTransformer:
    def test_adds_a_valid_flag_column_per_rule(self):
        df = pd.DataFrame({"age": [25, -5, 40]})
        result = ValidationTransformer().transform(df, rules={"age": lambda x: x >= 0})
        assert result["age_valid"].tolist() == [True, False, True]

    def test_missing_column_is_skipped_without_raising(self):
        df = pd.DataFrame({"age": [25]})
        result = ValidationTransformer().transform(df, rules={"missing": lambda x: True})
        assert "missing_valid" not in result.columns


class TestNormalizationTransformer:
    def test_minmax_scales_to_zero_one(self):
        df = pd.DataFrame({"a": [0.0, 5.0, 10.0]})
        result = NormalizationTransformer().transform(df, method="minmax")
        assert result["a"].tolist() == [0.0, 0.5, 1.0]

    def test_zscore_produces_zero_mean(self):
        df = pd.DataFrame({"a": [1.0, 2.0, 3.0]})
        result = NormalizationTransformer().transform(df, method="zscore")
        assert result["a"].mean() == pytest.approx(0.0, abs=1e-9)

    def test_constant_column_is_left_unchanged(self):
        df = pd.DataFrame({"a": [5.0, 5.0, 5.0]})
        result = NormalizationTransformer().transform(df, method="minmax")
        assert result["a"].tolist() == [5.0, 5.0, 5.0]


class TestFilterTransformer:
    def test_filters_rows_matching_all_conditions(self):
        df = pd.DataFrame({"age": [10, 20, 30]})
        result = FilterTransformer().transform(df, filters={"age": lambda x: x >= 20})
        assert result["age"].tolist() == [20, 30]

    def test_missing_column_is_skipped_without_raising(self):
        df = pd.DataFrame({"age": [10, 20]})
        result = FilterTransformer().transform(df, filters={"missing": lambda x: True})
        assert len(result) == 2


class TestEnrichmentTransformer:
    def test_adds_a_calculated_column(self):
        df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
        result = EnrichmentTransformer().transform(
            df, enrichments={"sum": lambda row: row["a"] + row["b"]}
        )
        assert result["sum"].tolist() == [4, 6]

    def test_failed_enrichment_is_logged_not_raised(self):
        df = pd.DataFrame({"a": [1, 2]})
        result = EnrichmentTransformer().transform(
            df, enrichments={"bad": lambda row: row["missing_column"]}
        )
        assert "bad" not in result.columns


class TestPipelineTransformer:
    def test_applies_transformations_in_order(self):
        df = pd.DataFrame({"a": [1, 1, 2]})
        pipeline = PipelineTransformer().add(DeduplicationTransformer())

        result = pipeline.transform(df)

        assert len(result) == 2

    def test_add_returns_self_for_chaining(self):
        pipeline = PipelineTransformer()
        assert pipeline.add(DeduplicationTransformer()) is pipeline
