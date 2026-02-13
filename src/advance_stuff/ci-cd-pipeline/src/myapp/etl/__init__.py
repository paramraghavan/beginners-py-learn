"""
ETL Package - Extract, Transform, Load

A complete ETL framework for data processing pipelines.
"""

from myapp.etl.pipeline import (
    APIExtractor,
    CSVExtractor,
    CSVLoader,
    DataFormat,
    ETLPipeline,
    Extractor,
    InMemoryExtractor,
    InMemoryLoader,
    JSONExtractor,
    JSONLoader,
    JSONLLoader,
    Loader,
    PipelineConfig,
    PipelineStats,
    Transformer,
    add_timestamp,
    clean_whitespace,
    compute_field,
    convert_types,
    create_sample_pipeline,
    filter_fields,
    filter_records,
    lowercase_keys,
    rename_fields,
    validate_required,
)

__all__ = [
    # Core classes
    "ETLPipeline",
    "PipelineConfig",
    "PipelineStats",
    "DataFormat",
    # Extractors
    "Extractor",
    "CSVExtractor",
    "JSONExtractor",
    "APIExtractor",
    "InMemoryExtractor",
    # Transformers
    "Transformer",
    "clean_whitespace",
    "lowercase_keys",
    "rename_fields",
    "filter_fields",
    "add_timestamp",
    "convert_types",
    "filter_records",
    "validate_required",
    "compute_field",
    # Loaders
    "Loader",
    "JSONLoader",
    "JSONLLoader",
    "CSVLoader",
    "InMemoryLoader",
    # Utilities
    "create_sample_pipeline",
]
