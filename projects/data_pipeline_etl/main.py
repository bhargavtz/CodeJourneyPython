#!/usr/bin/env python3
"""
Data Pipeline ETL Main Entry Point.

Run this script to execute the complete ETL pipeline.

Usage:
    python main.py                  # Run full pipeline
    python main.py --extract        # Extract only
    python main.py --transform      # Transform only
    python main.py --load           # Load only
    python main.py --debug          # Debug logging

Author: CodeJourney Data Project
License: MIT
"""

import os
import sys
import logging
import argparse
from pathlib import Path

import pandas as pd

from pipeline import Pipeline
from extractors import CSVExtractor, MultiSourceExtractor
from transformers import (
    DeduplicationTransformer,
    MissingValueTransformer,
    TypeConversionTransformer,
    NormalizationTransformer,
)
from loaders import CSVLoader, SQLiteLoader, MultiTargetLoader


# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(asctime)s - %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


class SamplePipeline(Pipeline):
    """Sample ETL pipeline implementation."""

    def __init__(self, config: dict):
        """
        Initialize sample pipeline.

        Args:
            config: Configuration dictionary
        """
        super().__init__("Sample Data Pipeline")
        self.config = config
        self.extractor = MultiSourceExtractor()
        self.loader = MultiTargetLoader()

    def extract(self) -> pd.DataFrame:
        """Extract data from configured sources."""
        sources = self.config.get("sources", [])

        if not sources:
            logger.warning("No sources configured. Using sample data.")
            # Create sample data
            return pd.DataFrame({
                "id": [1, 2, 3, 4, 5],
                "name": ["Alice", "Bob", "Charlie", "Alice", "Eve"],
                "age": [30, 25, 35, 30, 28],
                "email": ["alice@example.com", "bob@example.com", None, "alice@example.com", "eve@example.com"],
                "score": [85.5, 90.0, 75.5, 85.5, 92.0]
            })

        return self.extractor.extract_from_sources(sources)

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transform the data."""
        # Remove duplicates
        dedupe = DeduplicationTransformer()
        df = dedupe.transform(df)

        # Handle missing values
        missing = MissingValueTransformer()
        df = missing.transform(df, strategy="value", fill_value="unknown")

        # Type conversions
        conversions = TypeConversionTransformer()
        df = conversions.transform(df, conversions={"age": "int64"})

        # Normalize numeric columns
        normalizer = NormalizationTransformer()
        # Create a copy for normalization to avoid modifying original
        numeric_df = df.select_dtypes(include=["number"]).copy()
        if not numeric_df.empty:
            df[numeric_df.columns] = normalizer.transform(numeric_df)

        return df

    def load(self, df: pd.DataFrame) -> None:
        """Load data to configured targets."""
        targets = self.config.get("targets", [])

        if not targets:
            logger.info("No targets configured. Using default CSV output.")
            targets = [{
                "type": "csv",
                "path": "data/processed/output.csv"
            }]

        self.loader.load_to_targets(df, targets)


def create_sample_data():
    """Create sample data files for testing."""
    data_dir = Path("data/raw")
    data_dir.mkdir(parents=True, exist_ok=True)

    # Create sample CSV
    sample_df = pd.DataFrame({
        "id": [1, 2, 3, 4, 5, 6, 7, 8],
        "name": ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Henry"],
        "age": [30, 25, 35, 28, 28, 42, 31, 29],
        "email": ["alice@example.com", "bob@example.com", None, "david@example.com",
                  "eve@example.com", "frank@example.com", "grace@example.com", "henry@example.com"],
        "department": ["Sales", "IT", "HR", "Sales", "IT", "Finance", "HR", "Finance"],
        "salary": [50000, 60000, 45000, 55000, 62000, 75000, 48000, 58000]
    })

    csv_path = data_dir / "employees.csv"
    sample_df.to_csv(csv_path, index=False)
    logger.info(f"Created sample CSV: {csv_path}")

    return {
        "sources": [
            {
                "type": "csv",
                "path": str(csv_path),
                "options": {}
            }
        ],
        "targets": [
            {
                "type": "csv",
                "path": "data/processed/output.csv"
            },
            {
                "type": "sqlite",
                "path": "data/sql/pipeline.db",
                "options": {"table_name": "employees", "if_exists": "replace"}
            }
        ]
    }


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Data Pipeline ETL - Extract, Transform, Load",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Run full pipeline
  python main.py --extract          # Extract only
  python main.py --transform        # Transform only
  python main.py --load             # Load only
  python main.py --debug            # Run with debug logging
        """
    )

    parser.add_argument(
        "--extract",
        action="store_true",
        help="Run extract stage only"
    )
    parser.add_argument(
        "--transform",
        action="store_true",
        help="Run transform stage only"
    )
    parser.add_argument(
        "--load",
        action="store_true",
        help="Run load stage only"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )

    args = parser.parse_args()

    # Setup logging
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")

    try:
        logger.info("Initializing Data Pipeline...")

        # Create sample data if it doesn't exist
        config = create_sample_data()

        # Initialize pipeline
        pipeline = SamplePipeline(config)

        # Determine which stage(s) to run
        if args.extract:
            success = pipeline.run(stage="extract")
        elif args.transform:
            success = pipeline.run(stage="transform")
        elif args.load:
            success = pipeline.run(stage="load")
        else:
            # Run full pipeline
            success = pipeline.run()

        # Print status
        status = pipeline.get_status()
        logger.info(f"Pipeline Status: {status['status']}")
        logger.info(f"Success Rate: {status['success']}")

        sys.exit(0 if success else 1)

    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
