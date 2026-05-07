"""
Data transformation modules for ETL pipeline.

Provides transformations for common data cleaning and enrichment tasks:
- Removing duplicates
- Handling missing values
- Data validation
- Type conversion
- Normalization

Author: CodeJourney Data Project
License: MIT
"""

import logging
import pandas as pd
import numpy as np
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)


class Transformer:
    """Base class for data transformers."""

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transform data."""
        raise NotImplementedError


class DeduplicationTransformer(Transformer):
    """Remove duplicate rows."""

    def transform(self, df: pd.DataFrame, subset: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Remove duplicate rows.

        Args:
            df: Input DataFrame
            subset: Columns to check for duplicates

        Returns:
            DataFrame with duplicates removed
        """
        initial_rows = len(df)
        df = df.drop_duplicates(subset=subset, keep='first')
        removed = initial_rows - len(df)

        if removed > 0:
            logger.warning(f"Removed {removed} duplicate rows")

        return df


class MissingValueTransformer(Transformer):
    """Handle missing values."""

    def transform(
        self,
        df: pd.DataFrame,
        strategy: str = "mean",
        fill_value: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Handle missing values.

        Args:
            df: Input DataFrame
            strategy: 'drop', 'mean', 'forward_fill', 'value'
            fill_value: Value to use if strategy='value'

        Returns:
            DataFrame with missing values handled
        """
        missing_before = df.isnull().sum().sum()

        if strategy == "drop":
            df = df.dropna()
        elif strategy == "mean":
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
        elif strategy == "forward_fill":
            df = df.fillna(method="ffill")
        elif strategy == "value":
            if fill_value is None:
                raise ValueError("fill_value required for strategy='value'")
            df = df.fillna(fill_value)

        missing_after = df.isnull().sum().sum()
        removed = missing_before - missing_after

        if removed > 0:
            logger.info(f"Handled {removed} missing values")

        return df


class TypeConversionTransformer(Transformer):
    """Convert column data types."""

    def transform(self, df: pd.DataFrame, conversions: Dict[str, str]) -> pd.DataFrame:
        """
        Convert column data types.

        Args:
            df: Input DataFrame
            conversions: Dict of {column: target_type}

        Returns:
            DataFrame with converted types
        """
        for column, target_type in conversions.items():
            if column not in df.columns:
                logger.warning(f"Column {column} not found")
                continue

            try:
                if target_type == "datetime":
                    df[column] = pd.to_datetime(df[column])
                else:
                    df[column] = df[column].astype(target_type)
                logger.info(f"Converted {column} to {target_type}")
            except Exception as e:
                logger.error(f"Failed to convert {column} to {target_type}: {e}")

        return df


class ValidationTransformer(Transformer):
    """Validate data against rules."""

    def transform(self, df: pd.DataFrame, rules: Dict[str, callable]) -> pd.DataFrame:
        """
        Validate data and flag invalid rows.

        Args:
            df: Input DataFrame
            rules: Dict of {column: validation_function}

        Returns:
            DataFrame with validation flags
        """
        invalid_count = 0

        for column, rule in rules.items():
            if column not in df.columns:
                logger.warning(f"Column {column} not found for validation")
                continue

            # Apply validation rule
            mask = df[column].apply(rule)
            invalid = (~mask).sum()

            if invalid > 0:
                logger.warning(f"Found {invalid} invalid values in {column}")
                invalid_count += invalid

        return df


class NormalizationTransformer(Transformer):
    """Normalize numeric columns."""

    def transform(self, df: pd.DataFrame, method: str = "minmax") -> pd.DataFrame:
        """
        Normalize numeric columns.

        Args:
            df: Input DataFrame
            method: 'minmax' (0-1) or 'zscore' (standardized)

        Returns:
            DataFrame with normalized values
        """
        numeric_cols = df.select_dtypes(include=[np.number]).columns

        for col in numeric_cols:
            if method == "minmax":
                min_val = df[col].min()
                max_val = df[col].max()
                if max_val != min_val:
                    df[col] = (df[col] - min_val) / (max_val - min_val)
            elif method == "zscore":
                mean = df[col].mean()
                std = df[col].std()
                if std != 0:
                    df[col] = (df[col] - mean) / std

        logger.info(f"Normalized {len(numeric_cols)} numeric columns")
        return df


class FilterTransformer(Transformer):
    """Filter rows based on conditions."""

    def transform(self, df: pd.DataFrame, filters: Dict[str, callable]) -> pd.DataFrame:
        """
        Filter rows based on conditions.

        Args:
            df: Input DataFrame
            filters: Dict of {column: filter_function}

        Returns:
            Filtered DataFrame
        """
        initial_rows = len(df)

        for column, filter_fn in filters.items():
            if column not in df.columns:
                logger.warning(f"Column {column} not found for filtering")
                continue

            df = df[df[column].apply(filter_fn)]

        removed = initial_rows - len(df)
        if removed > 0:
            logger.info(f"Filtered out {removed} rows")

        return df


class EnrichmentTransformer(Transformer):
    """Add calculated/derived columns."""

    def transform(self, df: pd.DataFrame, enrichments: Dict[str, callable]) -> pd.DataFrame:
        """
        Add enrichment columns.

        Args:
            df: Input DataFrame
            enrichments: Dict of {new_column: calculation_function}

        Returns:
            DataFrame with new columns
        """
        for column, calc_fn in enrichments.items():
            try:
                df[column] = df.apply(calc_fn, axis=1)
                logger.info(f"Created enrichment column: {column}")
            except Exception as e:
                logger.error(f"Failed to create {column}: {e}")

        return df


class PipelineTransformer:
    """Compose multiple transformations."""

    def __init__(self):
        """Initialize transformer pipeline."""
        self.transformations: List[tuple] = []

    def add(self, transformer: Transformer, **kwargs) -> "PipelineTransformer":
        """
        Add transformation to pipeline.

        Args:
            transformer: Transformer instance
            **kwargs: Arguments for transformer

        Returns:
            Self for method chaining
        """
        self.transformations.append((transformer, kwargs))
        logger.info(f"Added {transformer.__class__.__name__} to pipeline")
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply all transformations in sequence.

        Args:
            df: Input DataFrame

        Returns:
            Transformed DataFrame
        """
        for transformer, kwargs in self.transformations:
            df = transformer.transform(df, **kwargs)

        logger.info(f"Applied {len(self.transformations)} transformations")
        return df
