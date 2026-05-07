"""
Core ETL Pipeline implementation.

Provides the main pipeline orchestration for Extract, Transform, Load operations
with comprehensive error handling, logging, and state management.

Author: CodeJourney Data Project
License: MIT
"""

import logging
import time
from typing import Optional, List, Dict, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import pandas as pd

logger = logging.getLogger(__name__)


class PipelineStatus(Enum):
    """Pipeline execution status."""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    PARTIAL_FAILURE = "partial_failure"
    FAILED = "failed"


@dataclass
class PipelineStatistics:
    """Statistics about pipeline execution."""
    start_time: float = 0.0
    end_time: float = 0.0
    rows_extracted: int = 0
    rows_transformed: int = 0
    rows_loaded: int = 0
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    @property
    def duration(self) -> float:
        """Get pipeline duration in seconds."""
        return self.end_time - self.start_time if self.end_time else 0.0

    @property
    def success_rate(self) -> float:
        """Get success rate (0-100)."""
        if self.rows_extracted == 0:
            return 0.0
        return (self.rows_loaded / self.rows_extracted) * 100

    def summary(self) -> str:
        """Get summary as formatted string."""
        return (
            f"\nPipeline Execution Summary:\n"
            f"  Status: {self.get_status()}\n"
            f"  Duration: {self.duration:.2f}s\n"
            f"  Rows Extracted: {self.rows_extracted}\n"
            f"  Rows Transformed: {self.rows_transformed}\n"
            f"  Rows Loaded: {self.rows_loaded}\n"
            f"  Success Rate: {self.success_rate:.1f}%\n"
            f"  Errors: {len(self.errors)}\n"
            f"  Warnings: {len(self.warnings)}\n"
        )

    def get_status(self) -> str:
        """Get overall status."""
        if not self.errors:
            return "SUCCESS"
        elif self.rows_loaded > 0:
            return "PARTIAL_FAILURE"
        else:
            return "FAILED"


class Pipeline:
    """
    Abstract base class for ETL pipelines.

    Subclasses should implement extract(), transform(), and load() methods.

    Attributes:
        name: Pipeline name
        status: Current execution status
        stats: Pipeline statistics
    """

    def __init__(self, name: str = "ETL Pipeline"):
        """
        Initialize pipeline.

        Args:
            name: Name for this pipeline
        """
        self.name = name
        self.status = PipelineStatus.PENDING
        self.stats = PipelineStatistics()
        self.data: Optional[pd.DataFrame] = None
        self.transformations: List[Callable] = []

        logger.info(f"Initialized {name}")

    def extract(self) -> pd.DataFrame:
        """
        Extract data from source systems.

        Must be implemented by subclasses.

        Returns:
            DataFrame with extracted data

        Raises:
            NotImplementedError: If not overridden by subclass
        """
        raise NotImplementedError("extract() must be implemented by subclass")

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform and clean data.

        Must be implemented by subclasses.

        Args:
            df: Input DataFrame

        Returns:
            Transformed DataFrame

        Raises:
            NotImplementedError: If not overridden by subclass
        """
        raise NotImplementedError("transform() must be implemented by subclass")

    def load(self, df: pd.DataFrame) -> None:
        """
        Load data to target systems.

        Must be implemented by subclasses.

        Args:
            df: DataFrame to load

        Raises:
            NotImplementedError: If not overridden by subclass
        """
        raise NotImplementedError("load() must be implemented by subclass")

    def add_transformation(self, transform_fn: Callable) -> "Pipeline":
        """
        Register a transformation function.

        Args:
            transform_fn: Function that takes/returns DataFrame

        Returns:
            Self for method chaining
        """
        self.transformations.append(transform_fn)
        logger.info(f"Registered transformation: {transform_fn.__name__}")
        return self

    def run(self, stage: Optional[str] = None) -> bool:
        """
        Execute the full ETL pipeline.

        Args:
            stage: Execute only specific stage (extract/transform/load)
                  If None, runs all stages

        Returns:
            True if successful, False if failed
        """
        self.status = PipelineStatus.RUNNING
        self.stats.start_time = time.time()

        try:
            # Extract
            if not stage or stage == "extract":
                logger.info("=" * 60)
                logger.info("Stage: EXTRACT")
                logger.info("=" * 60)
                self.data = self.extract()
                self.stats.rows_extracted = len(self.data) if self.data is not None else 0
                logger.info(f"Extracted {self.stats.rows_extracted} rows")

            # Transform
            if not stage or stage == "transform":
                if self.data is None:
                    raise ValueError("No data to transform. Run extract first.")

                logger.info("=" * 60)
                logger.info("Stage: TRANSFORM")
                logger.info("=" * 60)
                self.data = self.transform(self.data)

                # Apply registered transformations
                for transform_fn in self.transformations:
                    logger.info(f"Applying: {transform_fn.__name__}")
                    self.data = transform_fn(self.data)

                self.stats.rows_transformed = len(self.data)
                logger.info(f"Transformed to {self.stats.rows_transformed} rows")

            # Load
            if not stage or stage == "load":
                if self.data is None:
                    raise ValueError("No data to load. Run extract and transform first.")

                logger.info("=" * 60)
                logger.info("Stage: LOAD")
                logger.info("=" * 60)
                self.load(self.data)
                self.stats.rows_loaded = len(self.data)
                logger.info(f"Loaded {self.stats.rows_loaded} rows")

            self.status = PipelineStatus.SUCCESS
            logger.info("Pipeline completed successfully")
            return True

        except Exception as e:
            self.status = PipelineStatus.FAILED
            error_msg = f"Pipeline failed at {stage or 'unknown'} stage: {str(e)}"
            self.stats.errors.append(error_msg)
            logger.error(error_msg)
            return False

        finally:
            self.stats.end_time = time.time()
            logger.info(self.stats.summary())

    def validate_data(self, df: pd.DataFrame, rules: Dict[str, Callable]) -> bool:
        """
        Validate data against defined rules.

        Args:
            df: DataFrame to validate
            rules: Dict of {column: validation_function}

        Returns:
            True if all validations pass

        Raises:
            ValueError: If validation fails
        """
        for column, rule in rules.items():
            if column not in df.columns:
                raise ValueError(f"Column '{column}' not found in DataFrame")

            if not rule(df[column]):
                raise ValueError(f"Validation failed for column '{column}'")

        logger.info(f"Data validation passed for {len(rules)} columns")
        return True

    def get_status(self) -> Dict[str, Any]:
        """
        Get current pipeline status.

        Returns:
            Dictionary with status information
        """
        return {
            "name": self.name,
            "status": self.status.value,
            "rows_extracted": self.stats.rows_extracted,
            "rows_transformed": self.stats.rows_transformed,
            "rows_loaded": self.stats.rows_loaded,
            "duration": self.stats.duration,
            "success": self.status == PipelineStatus.SUCCESS,
        }

    def handle_error(self, error: Exception, action: str = "log") -> None:
        """
        Handle pipeline errors.

        Args:
            error: Exception that occurred
            action: How to handle (log/raise/skip)
        """
        error_msg = str(error)
        self.stats.errors.append(error_msg)

        if action == "log":
            logger.warning(f"Error (non-fatal): {error_msg}")
        elif action == "raise":
            logger.error(f"Error (fatal): {error_msg}")
            raise error
        elif action == "skip":
            logger.info(f"Skipping error: {error_msg}")
