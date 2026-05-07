"""
Data Pipeline ETL - Mountain Peak Project.

Extract, Transform, Load pipeline for data processing and integration.
"""

from .pipeline import Pipeline, PipelineStatus, PipelineStatistics
from .extractors import Extractor, CSVExtractor, JSONExtractor, SQLExtractor, MultiSourceExtractor
from .transformers import (
    Transformer,
    DeduplicationTransformer,
    MissingValueTransformer,
    TypeConversionTransformer,
    ValidationTransformer,
    NormalizationTransformer,
    FilterTransformer,
    EnrichmentTransformer,
    PipelineTransformer,
)
from .loaders import Loader, CSVLoader, SQLiteLoader, JSONLoader, MultiTargetLoader

__version__ = "0.1.0"
__author__ = "CodeJourney"
__all__ = [
    "Pipeline",
    "PipelineStatus",
    "PipelineStatistics",
    "Extractor",
    "CSVExtractor",
    "JSONExtractor",
    "SQLExtractor",
    "MultiSourceExtractor",
    "Transformer",
    "DeduplicationTransformer",
    "MissingValueTransformer",
    "TypeConversionTransformer",
    "ValidationTransformer",
    "NormalizationTransformer",
    "FilterTransformer",
    "EnrichmentTransformer",
    "PipelineTransformer",
    "Loader",
    "CSVLoader",
    "SQLiteLoader",
    "JSONLoader",
    "MultiTargetLoader",
]
