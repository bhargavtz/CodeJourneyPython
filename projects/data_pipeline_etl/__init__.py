"""
Data Pipeline ETL - Mountain Peak Project.

Extract, Transform, Load pipeline for data processing and integration.
"""

from .extractors import CSVExtractor, Extractor, JSONExtractor, MultiSourceExtractor, SQLExtractor
from .loaders import CSVLoader, JSONLoader, Loader, MultiTargetLoader, SQLiteLoader
from .pipeline import Pipeline, PipelineStatistics, PipelineStatus
from .transformers import (
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
