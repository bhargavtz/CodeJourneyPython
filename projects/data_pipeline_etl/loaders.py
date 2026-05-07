"""
Data loading modules for ETL pipeline.

Provides loaders for common target systems:
- CSV files
- SQLite databases
- JSON files

Author: CodeJourney Data Project
License: MIT
"""

import logging
import pandas as pd
import sqlite3
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class Loader:
    """Base class for data loaders."""

    def load(self, df: pd.DataFrame, target: str, **kwargs) -> None:
        """Load data to target."""
        raise NotImplementedError


class CSVLoader(Loader):
    """Load data to CSV file."""

    def load(self, df: pd.DataFrame, target: str, index: bool = False, **kwargs) -> None:
        """
        Write DataFrame to CSV.

        Args:
            df: DataFrame to load
            target: CSV file path
            index: Whether to write index (default: False)
            **kwargs: Additional pandas to_csv arguments
        """
        try:
            path = Path(target)
            path.parent.mkdir(parents=True, exist_ok=True)

            df.to_csv(target, index=index, **kwargs)
            logger.info(f"Loaded {len(df)} rows to CSV: {target}")
        except Exception as e:
            logger.error(f"Error loading to CSV {target}: {e}")
            raise


class SQLiteLoader(Loader):
    """Load data to SQLite database."""

    def load(
        self,
        df: pd.DataFrame,
        target: str,
        table_name: str = "data",
        if_exists: str = "replace",
        **kwargs
    ) -> None:
        """
        Write DataFrame to SQLite.

        Args:
            df: DataFrame to load
            target: Database file path
            table_name: Target table name
            if_exists: 'replace', 'append', or 'fail'
            **kwargs: Additional pandas to_sql arguments
        """
        try:
            path = Path(target)
            path.parent.mkdir(parents=True, exist_ok=True)

            conn = sqlite3.connect(target)
            df.to_sql(table_name, conn, if_exists=if_exists, index=False, **kwargs)
            conn.close()

            logger.info(f"Loaded {len(df)} rows to SQLite: {target}/{table_name}")
        except Exception as e:
            logger.error(f"Error loading to SQLite {target}: {e}")
            raise


class JSONLoader(Loader):
    """Load data to JSON file."""

    def load(
        self,
        df: pd.DataFrame,
        target: str,
        orient: str = "records",
        **kwargs
    ) -> None:
        """
        Write DataFrame to JSON.

        Args:
            df: DataFrame to load
            target: JSON file path
            orient: 'records', 'split', 'index', 'columns', 'values'
            **kwargs: Additional pandas to_json arguments
        """
        try:
            path = Path(target)
            path.parent.mkdir(parents=True, exist_ok=True)

            df.to_json(target, orient=orient, **kwargs)
            logger.info(f"Loaded {len(df)} rows to JSON: {target}")
        except Exception as e:
            logger.error(f"Error loading to JSON {target}: {e}")
            raise


class MultiTargetLoader:
    """Load to multiple targets simultaneously."""

    def __init__(self):
        """Initialize multi-target loader."""
        self.loaders = {
            "csv": CSVLoader(),
            "sqlite": SQLiteLoader(),
            "json": JSONLoader(),
        }

    def load_to_targets(self, df: pd.DataFrame, targets: list) -> None:
        """
        Load DataFrame to multiple targets.

        Args:
            df: DataFrame to load
            targets: List of target configs, each with:
                - type: 'csv', 'sqlite', or 'json'
                - path: Target file path
                - options: Optional loader options

        Raises:
            ValueError: If target type unknown
        """
        for target in targets:
            target_type = target.get("type")
            target_path = target.get("path")
            options = target.get("options", {})

            if target_type not in self.loaders:
                raise ValueError(f"Unknown target type: {target_type}")

            loader = self.loaders[target_type]
            loader.load(df, target_path, **options)

        logger.info(f"Data loaded to {len(targets)} targets")
