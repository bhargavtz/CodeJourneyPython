"""
Feature engineering for recommendation systems.

Implements feature creation and transformation functions for ML models.

Author: CodeJourney ML Project
License: MIT
"""

import logging
import pandas as pd
import numpy as np
from typing import Dict, Tuple

logger = logging.getLogger(__name__)


class FeatureEngineering:
    """Feature engineering operations for recommendation systems."""

    @staticmethod
    def create_user_features(df: pd.DataFrame, user_id_col: str = "user_id",
                             rating_col: str = "rating") -> pd.DataFrame:
        """
        Create user-level features.

        Args:
            df: Input dataframe with user-item ratings
            user_id_col: Name of user ID column
            rating_col: Name of rating column

        Returns:
            DataFrame with user features
        """
        user_features = df.groupby(user_id_col)[rating_col].agg([
            ("mean_rating", "mean"),
            ("num_ratings", "count"),
            ("std_rating", "std"),
            ("min_rating", "min"),
            ("max_rating", "max"),
        ]).fillna(0)

        user_features["bias"] = user_features["mean_rating"] - df[rating_col].mean()
        user_features["activity_level"] = pd.qcut(user_features["num_ratings"],
                                                   q=4, labels=False, duplicates='drop')

        logger.info(f"Created features for {len(user_features)} users")
        return user_features

    @staticmethod
    def create_item_features(df: pd.DataFrame, item_id_col: str = "item_id",
                             rating_col: str = "rating") -> pd.DataFrame:
        """
        Create item-level features.

        Args:
            df: Input dataframe
            item_id_col: Name of item ID column
            rating_col: Name of rating column

        Returns:
            DataFrame with item features
        """
        item_features = df.groupby(item_id_col)[rating_col].agg([
            ("mean_rating", "mean"),
            ("num_ratings", "count"),
            ("std_rating", "std"),
            ("min_rating", "min"),
            ("max_rating", "max"),
        ]).fillna(0)

        item_features["popularity"] = pd.qcut(item_features["num_ratings"],
                                              q=4, labels=False, duplicates='drop')
        item_features["quality"] = (item_features["mean_rating"] -
                                   df[rating_col].min()) / (df[rating_col].max() -
                                                           df[rating_col].min())

        logger.info(f"Created features for {len(item_features)} items")
        return item_features

    @staticmethod
    def create_interaction_features(df: pd.DataFrame,
                                   user_id_col: str = "user_id",
                                   item_id_col: str = "item_id",
                                   rating_col: str = "rating") -> pd.DataFrame:
        """
        Create user-item interaction features.

        Args:
            df: Input dataframe
            user_id_col: Name of user ID column
            item_id_col: Name of item ID column
            rating_col: Name of rating column

        Returns:
            DataFrame with interaction features
        """
        interactions = df.copy()

        # User-specific item rating compared to item average
        item_means = df.groupby(item_id_col)[rating_col].transform("mean")
        interactions["user_item_diff"] = interactions[rating_col] - item_means

        # Item popularity from user perspective
        user_rating_counts = df.groupby(user_id_col).size()
        interactions["user_rating_density"] = interactions[user_id_col].map(
            user_rating_counts / len(df)
        )

        logger.info("Created interaction features")
        return interactions

    @staticmethod
    def normalize_features(X: np.ndarray, return_params: bool = False) -> Tuple:
        """
        Normalize features to [0, 1] range.

        Args:
            X: Input feature array
            return_params: If True, return min/max for later denormalization

        Returns:
            Normalized array, or (normalized array, (min, max)) if return_params=True
        """
        X_min = X.min(axis=0)
        X_max = X.max(axis=0)
        X_range = X_max - X_min
        X_range[X_range == 0] = 1  # Avoid division by zero

        X_normalized = (X - X_min) / X_range

        if return_params:
            return X_normalized, (X_min, X_max)
        return X_normalized

    @staticmethod
    def standardize_features(X: np.ndarray, return_params: bool = False) -> Tuple:
        """
        Standardize features (mean 0, std 1).

        Args:
            X: Input feature array
            return_params: If True, return mean/std for later standardization

        Returns:
            Standardized array, or (standardized array, (mean, std)) if return_params=True
        """
        X_mean = X.mean(axis=0)
        X_std = X.std(axis=0)
        X_std[X_std == 0] = 1  # Avoid division by zero

        X_standardized = (X - X_mean) / X_std

        if return_params:
            return X_standardized, (X_mean, X_std)
        return X_standardized

    @staticmethod
    def create_temporal_features(df: pd.DataFrame,
                                timestamp_col: str = "timestamp") -> pd.DataFrame:
        """
        Create time-based features.

        Args:
            df: Input dataframe with timestamp
            timestamp_col: Name of timestamp column

        Returns:
            DataFrame with temporal features
        """
        df = df.copy()

        if timestamp_col not in df.columns:
            logger.warning(f"Column {timestamp_col} not found. Skipping temporal features.")
            return df

        df[timestamp_col] = pd.to_datetime(df[timestamp_col])
        df["day_of_week"] = df[timestamp_col].dt.dayofweek
        df["month"] = df[timestamp_col].dt.month
        df["quarter"] = df[timestamp_col].dt.quarter
        df["hour"] = df[timestamp_col].dt.hour

        logger.info("Created temporal features")
        return df

    @staticmethod
    def handle_missing_values(df: pd.DataFrame, strategy: str = "mean") -> pd.DataFrame:
        """
        Handle missing values in features.

        Args:
            df: Input dataframe
            strategy: 'mean', 'median', 'forward_fill', 'drop'

        Returns:
            DataFrame with missing values handled
        """
        missing_before = df.isnull().sum().sum()

        if strategy == "mean":
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
        elif strategy == "median":
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
        elif strategy == "forward_fill":
            df = df.fillna(method="ffill")
        elif strategy == "drop":
            df = df.dropna()

        missing_after = df.isnull().sum().sum()
        logger.info(f"Handled {missing_before - missing_after} missing values")

        return df


class FeaturePipeline:
    """Pipeline for feature engineering workflow."""

    def __init__(self):
        """Initialize feature pipeline."""
        self.fe = FeatureEngineering()
        self.user_features = None
        self.item_features = None

    def fit_transform(self, df: pd.DataFrame,
                     user_id_col: str = "user_id",
                     item_id_col: str = "item_id",
                     rating_col: str = "rating") -> pd.DataFrame:
        """
        Fit and transform features.

        Args:
            df: Input dataframe
            user_id_col: User ID column name
            item_id_col: Item ID column name
            rating_col: Rating column name

        Returns:
            DataFrame with engineered features
        """
        # Create features
        self.user_features = self.fe.create_user_features(df, user_id_col, rating_col)
        self.item_features = self.fe.create_item_features(df, item_id_col, rating_col)

        # Add temporal features if timestamp exists
        if "timestamp" in df.columns:
            df = self.fe.create_temporal_features(df)

        # Handle missing values
        df = self.fe.handle_missing_values(df, strategy="mean")

        logger.info("Feature engineering pipeline completed")
        return df
