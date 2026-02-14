"""
ETL Pipeline - Extract, Transform, Load

A sample ETL application demonstrating data processing workflows.
This module provides the core ETL pipeline functionality.
"""

import json
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable

import httpx

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataFormat(Enum):
    """Supported data formats."""

    CSV = "csv"
    JSON = "json"
    JSONL = "jsonl"


@dataclass
class PipelineConfig:
    """Configuration for ETL pipeline."""

    name: str = "default"
    batch_size: int = 1000
    fail_on_error: bool = False
    log_level: str = "INFO"
    output_dir: Path = field(default_factory=lambda: Path("output"))


@dataclass
class PipelineStats:
    """Statistics for pipeline execution."""

    records_extracted: int = 0
    records_transformed: int = 0
    records_loaded: int = 0
    records_failed: int = 0
    start_time: datetime | None = None
    end_time: datetime | None = None

    @property
    def duration_seconds(self) -> float:
        """Calculate pipeline duration in seconds."""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0.0

    @property
    def success_rate(self) -> float:
        """Calculate success rate as percentage."""
        total = self.records_extracted
        if total == 0:
            return 100.0
        return ((total - self.records_failed) / total) * 100

    def to_dict(self) -> dict[str, Any]:
        """Convert stats to dictionary."""
        return {
            "records_extracted": self.records_extracted,
            "records_transformed": self.records_transformed,
            "records_loaded": self.records_loaded,
            "records_failed": self.records_failed,
            "duration_seconds": self.duration_seconds,
            "success_rate": self.success_rate,
        }


# =============================================================================
# Extractors
# =============================================================================


class Extractor(ABC):
    """Base class for data extractors."""

    @abstractmethod
    def extract(self) -> list[dict[str, Any]]:
        """Extract data from source."""
        pass


class CSVExtractor(Extractor):
    """Extract data from CSV files."""

    def __init__(self, filepath: str | Path, delimiter: str = ","):
        self.filepath = Path(filepath)
        self.delimiter = delimiter

    def extract(self) -> list[dict[str, Any]]:
        """Extract data from CSV file."""
        if not self.filepath.exists():
            raise FileNotFoundError(f"CSV file not found: {self.filepath}")

        records = []
        with open(self.filepath, encoding="utf-8") as f:
            lines = f.readlines()
            if not lines:
                return []

            # Parse header
            headers = [h.strip().strip('"') for h in lines[0].split(self.delimiter)]

            # Parse data rows
            for line in lines[1:]:
                if line.strip():
                    values = [v.strip().strip('"') for v in line.split(self.delimiter)]
                    record = dict(zip(headers, values))
                    records.append(record)

        logger.info(f"Extracted {len(records)} records from {self.filepath}")
        return records


class JSONExtractor(Extractor):
    """Extract data from JSON files."""

    def __init__(self, filepath: str | Path):
        self.filepath = Path(filepath)

    def extract(self) -> list[dict[str, Any]]:
        """Extract data from JSON file."""
        if not self.filepath.exists():
            raise FileNotFoundError(f"JSON file not found: {self.filepath}")

        with open(self.filepath, encoding="utf-8") as f:
            data = json.load(f)

        # Handle both array and object with data key
        if isinstance(data, list):
            records = data
        elif isinstance(data, dict):
            records = data.get("data", data.get("records", [data]))
        else:
            records = [data]

        logger.info(f"Extracted {len(records)} records from {self.filepath}")
        return records


class APIExtractor(Extractor):
    """Extract data from REST API."""

    def __init__(
        self,
        url: str,
        headers: dict[str, str] | None = None,
        params: dict[str, str] | None = None,
        data_key: str | None = None,
    ):
        self.url = url
        self.headers = headers or {}
        self.params = params or {}
        self.data_key = data_key

    def extract(self) -> list[dict[str, Any]]:
        """Extract data from API endpoint."""
        try:
            with httpx.Client() as client:
                response = client.get(
                    self.url, headers=self.headers, params=self.params, timeout=30.0
                )
                response.raise_for_status()
                data = response.json()

            # Extract records from response
            if self.data_key and isinstance(data, dict):
                records = data.get(self.data_key, [])
            elif isinstance(data, list):
                records = data
            else:
                records = [data]

            logger.info(f"Extracted {len(records)} records from {self.url}")
            return records

        except httpx.HTTPError as e:
            logger.error(f"API extraction failed: {e}")
            raise


class InMemoryExtractor(Extractor):
    """Extract data from in-memory data (useful for testing)."""

    def __init__(self, data: list[dict[str, Any]]):
        self.data = data

    def extract(self) -> list[dict[str, Any]]:
        """Return in-memory data."""
        logger.info(f"Extracted {len(self.data)} records from memory")
        return self.data.copy()


# =============================================================================
# Transformers
# =============================================================================


class Transformer:
    """Data transformer with chainable transformations."""

    def __init__(self) -> None:
        self._transformations: list[Callable[[dict], dict | None]] = []

    def add(self, func: Callable[[dict], dict | None]) -> "Transformer":
        """Add a transformation function."""
        self._transformations.append(func)
        return self

    def transform(self, records: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Apply all transformations to records."""
        result = []
        for record in records:
            transformed = record
            skip = False
            for func in self._transformations:
                if transformed is None:
                    skip = True
                    break
                transformed = func(transformed)
            if not skip and transformed is not None:
                result.append(transformed)

        logger.info(
            f"Transformed {len(records)} records -> {len(result)} records"
        )
        return result


# Common transformation functions
def clean_whitespace(record: dict[str, Any]) -> dict[str, Any]:
    """Remove leading/trailing whitespace from string values."""
    return {
        k: v.strip() if isinstance(v, str) else v
        for k, v in record.items()
    }


def lowercase_keys(record: dict[str, Any]) -> dict[str, Any]:
    """Convert all keys to lowercase."""
    return {k.lower(): v for k, v in record.items()}


def rename_fields(mapping: dict[str, str]) -> Callable[[dict], dict]:
    """Create a function that renames fields."""
    def _rename(record: dict[str, Any]) -> dict[str, Any]:
        return {mapping.get(k, k): v for k, v in record.items()}
    return _rename


def filter_fields(fields: list[str]) -> Callable[[dict], dict]:
    """Create a function that keeps only specified fields."""
    def _filter(record: dict[str, Any]) -> dict[str, Any]:
        return {k: v for k, v in record.items() if k in fields}
    return _filter


def add_timestamp(field_name: str = "processed_at") -> Callable[[dict], dict]:
    """Create a function that adds a timestamp field."""
    def _add_ts(record: dict[str, Any]) -> dict[str, Any]:
        record[field_name] = datetime.now().isoformat()
        return record
    return _add_ts


def convert_types(type_map: dict[str, type]) -> Callable[[dict], dict]:
    """Create a function that converts field types."""
    def _convert(record: dict[str, Any]) -> dict[str, Any]:
        result = record.copy()
        for field, target_type in type_map.items():
            if field in result and result[field] is not None:
                try:
                    if target_type == bool:
                        result[field] = str(result[field]).lower() in ("true", "1", "yes")
                    else:
                        result[field] = target_type(result[field])
                except (ValueError, TypeError):
                    pass  # Keep original value if conversion fails
        return result
    return _convert


def filter_records(
    condition: Callable[[dict], bool]
) -> Callable[[dict], dict | None]:
    """Create a function that filters records based on condition."""
    def _filter(record: dict[str, Any]) -> dict[str, Any] | None:
        return record if condition(record) else None
    return _filter


def validate_required(
    fields: list[str]
) -> Callable[[dict], dict | None]:
    """Create a function that validates required fields."""
    def _validate(record: dict[str, Any]) -> dict[str, Any] | None:
        for field in fields:
            if field not in record or record[field] is None or record[field] == "":
                return None
        return record
    return _validate


def compute_field(
    field_name: str, func: Callable[[dict], Any]
) -> Callable[[dict], dict]:
    """Create a function that computes a new field."""
    def _compute(record: dict[str, Any]) -> dict[str, Any]:
        record[field_name] = func(record)
        return record
    return _compute


# =============================================================================
# Loaders
# =============================================================================


class Loader(ABC):
    """Base class for data loaders."""

    @abstractmethod
    def load(self, records: list[dict[str, Any]]) -> int:
        """Load data to destination. Returns number of records loaded."""
        pass


class JSONLoader(Loader):
    """Load data to JSON file."""

    def __init__(self, filepath: str | Path, indent: int = 2):
        self.filepath = Path(filepath)
        self.indent = indent

    def load(self, records: list[dict[str, Any]]) -> int:
        """Write records to JSON file."""
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=self.indent, default=str)
        logger.info(f"Loaded {len(records)} records to {self.filepath}")
        return len(records)


class JSONLLoader(Loader):
    """Load data to JSON Lines file."""

    def __init__(self, filepath: str | Path):
        self.filepath = Path(filepath)

    def load(self, records: list[dict[str, Any]]) -> int:
        """Write records to JSONL file."""
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(self.filepath, "w", encoding="utf-8") as f:
            for record in records:
                f.write(json.dumps(record, default=str) + "\n")
        logger.info(f"Loaded {len(records)} records to {self.filepath}")
        return len(records)


class CSVLoader(Loader):
    """Load data to CSV file."""

    def __init__(self, filepath: str | Path, delimiter: str = ","):
        self.filepath = Path(filepath)
        self.delimiter = delimiter

    def load(self, records: list[dict[str, Any]]) -> int:
        """Write records to CSV file."""
        if not records:
            return 0

        self.filepath.parent.mkdir(parents=True, exist_ok=True)

        # Get all unique headers
        headers = list(records[0].keys())

        with open(self.filepath, "w", encoding="utf-8") as f:
            # Write header
            f.write(self.delimiter.join(headers) + "\n")
            # Write data
            for record in records:
                values = [str(record.get(h, "")) for h in headers]
                f.write(self.delimiter.join(values) + "\n")

        logger.info(f"Loaded {len(records)} records to {self.filepath}")
        return len(records)


class InMemoryLoader(Loader):
    """Load data to memory (useful for testing)."""

    def __init__(self) -> None:
        self.data: list[dict[str, Any]] = []

    def load(self, records: list[dict[str, Any]]) -> int:
        """Store records in memory."""
        self.data.extend(records)
        logger.info(f"Loaded {len(records)} records to memory")
        return len(records)

    def get_data(self) -> list[dict[str, Any]]:
        """Get loaded data."""
        return self.data.copy()

    def clear(self) -> None:
        """Clear loaded data."""
        self.data = []


# =============================================================================
# ETL Pipeline
# =============================================================================


class ETLPipeline:
    """Main ETL Pipeline orchestrator."""

    def __init__(self, config: PipelineConfig | None = None):
        self.config = config or PipelineConfig()
        self.extractor: Extractor | None = None
        self.transformer: Transformer | None = None
        self.loader: Loader | None = None
        self.stats = PipelineStats()

    def extract_from(self, extractor: Extractor) -> "ETLPipeline":
        """Set the extractor."""
        self.extractor = extractor
        return self

    def transform_with(self, transformer: Transformer) -> "ETLPipeline":
        """Set the transformer."""
        self.transformer = transformer
        return self

    def load_to(self, loader: Loader) -> "ETLPipeline":
        """Set the loader."""
        self.loader = loader
        return self

    def run(self) -> PipelineStats:
        """Execute the ETL pipeline."""
        if not self.extractor:
            raise ValueError("No extractor configured")
        if not self.loader:
            raise ValueError("No loader configured")

        logger.info(f"Starting ETL pipeline: {self.config.name}")
        self.stats = PipelineStats()
        self.stats.start_time = datetime.now()

        try:
            # Extract
            logger.info("Phase 1: Extracting data...")
            records = self.extractor.extract()
            self.stats.records_extracted = len(records)

            # Transform
            if self.transformer:
                logger.info("Phase 2: Transforming data...")
                records = self.transformer.transform(records)
            self.stats.records_transformed = len(records)

            # Load
            logger.info("Phase 3: Loading data...")
            loaded = self.loader.load(records)
            self.stats.records_loaded = loaded

        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            self.stats.records_failed = self.stats.records_extracted
            if self.config.fail_on_error:
                raise

        finally:
            self.stats.end_time = datetime.now()
            logger.info(
                f"Pipeline complete: {self.stats.records_loaded} records loaded "
                f"in {self.stats.duration_seconds:.2f}s"
            )

        return self.stats


def create_sample_pipeline(
    input_file: str | Path,
    output_file: str | Path,
    input_format: DataFormat = DataFormat.JSON,
    output_format: DataFormat = DataFormat.JSON,
) -> ETLPipeline:
    """Create a sample ETL pipeline with common transformations."""

    # Create extractor based on input format
    if input_format == DataFormat.CSV:
        extractor = CSVExtractor(input_file)
    else:
        extractor = JSONExtractor(input_file)

    # Create transformer with common operations
    transformer = (
        Transformer()
        .add(clean_whitespace)
        .add(lowercase_keys)
        .add(add_timestamp("_etl_processed_at"))
    )

    # Create loader based on output format
    if output_format == DataFormat.CSV:
        loader = CSVLoader(output_file)
    elif output_format == DataFormat.JSONL:
        loader = JSONLLoader(output_file)
    else:
        loader = JSONLoader(output_file)

    # Build pipeline
    pipeline = (
        ETLPipeline(PipelineConfig(name="sample-pipeline"))
        .extract_from(extractor)
        .transform_with(transformer)
        .load_to(loader)
    )

    return pipeline
