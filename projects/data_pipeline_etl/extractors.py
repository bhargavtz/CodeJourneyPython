"""
Data extraction modules for ETL pipeline.

Provides extractors for common data sources:
- CSV files
- JSON files
- Databases (SQLite, PostgreSQL)

Author: CodeJourney Data Project
License: MIT
"""

import logging
import pandas as pd
from typing import Optional, List
from pathlib import Path

logger = logging.getLogger(__name__)


class Extractor:
    """Base class for data extractors."""

    def extract(self, source: str, **kwargs) -> pd.DataFrame:
        """Extract data from source."""
        raise NotImplementedError


class CSVExtractor(Extractor):
    """Extract data from CSV files."""

    def extract(
        self,
        source: str,
        encoding: str = "utf-8",
        dtype: Optional[dict] = None,
        **kwargs
    ) -> pd.DataFrame:
        """
        Read CSV file.

        Args:
            source: Path to CSV file
            encoding: File encoding (default: utf-8)
            dtype: Column data types
            **kwargs: Additional pandas read_csv arguments

        Returns:
            DataFrame with CSV data

        Raises:
            FileNotFoundError: If file doesn't exist
            pd.errors.ParserError: If CSV is malformed
        """
        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(f"CSV file not found: {source}")

        try:
            logger.info(f"Extracting from CSV: {source}")
            df = pd.read_csv(source, encoding=encoding, dtype=dtype, **kwargs)
            logger.info(f"Read {len(df)} rows from {source}")
            return df
        except pd.errors.ParserError as e:
            logger.error(f"Error parsing CSV {source}: {e}")
            raise


class JSONExtractor(Extractor):
    """Extract data from JSON files."""

    def extract(
        self,
        source: str,
        lines: bool = False,
        **kwargs
    ) -> pd.DataFrame:
        """
        Read JSON file.

        Args:
            source: Path to JSON file
            lines: If True, read as JSON Lines (one record per line)
            **kwargs: Additional pandas read_json arguments

        Returns:
            DataFrame with JSON data

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If JSON is invalid
        """
        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(f"JSON file not found: {source}")

        try:
            logger.info(f"Extracting from JSON: {source}")
            df = pd.read_json(source, lines=lines, **kwargs)
            logger.info(f"Read {len(df)} rows from {source}")
            return df
        except ValueError as e:
            logger.error(f"Error parsing JSON {source}: {e}")
            raise


class SQLExtractor(Extractor):
    """Extract data from SQL databases."""

    def extract(
        self,
        source: str,
        query: str,
        connection=None,
        **kwargs
    ) -> pd.DataFrame:
        """
        Read data from database.

        Args:
            source: Database connection string
            query: SQL query to execute
            connection: Optional pre-configured connection
            **kwargs: Additional pandas read_sql arguments

        Returns:
            DataFrame with query results

        Raises:
            ValueError: If connection fails
        """
        try:
            logger.info(f"Executing SQL query from: {source}")
            if connection is None:
                raise ValueError("Database connection required")

            df = pd.read_sql(query, connection, **kwargs)
            logger.info(f"Read {len(df)} rows from database")
            return df
        except Exception as e:
            logger.error(f"Database error: {e}")
            raise


class MultiSourceExtractor:
    """Extract from multiple sources and combine."""

    def __init__(self):
        """Initialize multi-source extractor."""
        self.extractors = {
            "csv": CSVExtractor(),
            "json": JSONExtractor(),
            "sql": SQLExtractor(),
        }

    def extract_from_sources(
        self,
        sources: List[dict],
        combine: str = "concat"
    ) -> pd.DataFrame:
        """
        Extract from multiple sources.

        Args:
            sources: List of source configs, each with:
                - type: 'csv', 'json', or 'sql'
                - path: Source path or query
                - options: Optional extractor options
            combine: How to combine ('concat', 'merge')

        Returns:
            Combined DataFrame

        Raises:
            ValueError: If source type unknown
        """
        dfs = []

        for source in sources:
            source_type = source.get("type")
            source_path = source.get("path")
            options = source.get("options", {})

            if source_type not in self.extractors:
                raise ValueError(f"Unknown source type: {source_type}")

            extractor = self.extractors[source_type]
            df = extractor.extract(source_path, **options)
            dfs.append(df)

        if not dfs:
            return pd.DataFrame()

        if combine == "concat":
            result = pd.concat(dfs, ignore_index=True)
        elif combine == "merge":
            result = dfs[0]
            for df in dfs[1:]:
                result = result.merge(df)
        else:
            raise ValueError(f"Unknown combine method: {combine}")

        logger.info(f"Combined {len(dfs)} sources: {len(result)} total rows")
        return result
