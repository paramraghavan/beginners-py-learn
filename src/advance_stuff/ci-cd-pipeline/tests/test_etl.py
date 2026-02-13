"""
Tests for myapp.etl.pipeline module
"""

import json
from pathlib import Path

import pytest

from myapp.etl import (
    CSVExtractor,
    CSVLoader,
    ETLPipeline,
    InMemoryExtractor,
    InMemoryLoader,
    JSONExtractor,
    JSONLoader,
    JSONLLoader,
    PipelineConfig,
    PipelineStats,
    Transformer,
    add_timestamp,
    clean_whitespace,
    compute_field,
    convert_types,
    filter_fields,
    filter_records,
    lowercase_keys,
    rename_fields,
    validate_required,
)


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def sample_records():
    """Sample records for testing."""
    return [
        {"Name": "Alice", "Age": "25", "City": "NYC"},
        {"Name": "Bob", "Age": "30", "City": "LA"},
        {"Name": "Carol", "Age": "35", "City": "Chicago"},
    ]


@pytest.fixture
def sample_json_file(tmp_path, sample_records):
    """Create a temporary JSON file."""
    filepath = tmp_path / "test_data.json"
    with open(filepath, "w") as f:
        json.dump(sample_records, f)
    return filepath


@pytest.fixture
def sample_json_with_data_key(tmp_path, sample_records):
    """Create a temporary JSON file with data key."""
    filepath = tmp_path / "test_data_key.json"
    with open(filepath, "w") as f:
        json.dump({"data": sample_records}, f)
    return filepath


@pytest.fixture
def sample_csv_file(tmp_path):
    """Create a temporary CSV file."""
    filepath = tmp_path / "test_data.csv"
    content = """Name,Age,City
Alice,25,NYC
Bob,30,LA
Carol,35,Chicago"""
    filepath.write_text(content)
    return filepath


# =============================================================================
# Extractor Tests
# =============================================================================


class TestJSONExtractor:
    """Tests for JSONExtractor."""

    def test_extract_json_array(self, sample_json_file):
        """Test extracting JSON array."""
        extractor = JSONExtractor(sample_json_file)
        records = extractor.extract()
        assert len(records) == 3
        assert records[0]["Name"] == "Alice"

    def test_extract_json_with_data_key(self, sample_json_with_data_key):
        """Test extracting JSON with data key."""
        extractor = JSONExtractor(sample_json_with_data_key)
        records = extractor.extract()
        assert len(records) == 3

    def test_extract_nonexistent_file(self, tmp_path):
        """Test extracting from nonexistent file."""
        extractor = JSONExtractor(tmp_path / "nonexistent.json")
        with pytest.raises(FileNotFoundError):
            extractor.extract()


class TestCSVExtractor:
    """Tests for CSVExtractor."""

    def test_extract_csv(self, sample_csv_file):
        """Test extracting CSV data."""
        extractor = CSVExtractor(sample_csv_file)
        records = extractor.extract()
        assert len(records) == 3
        assert records[0]["Name"] == "Alice"
        assert records[0]["Age"] == "25"

    def test_extract_empty_csv(self, tmp_path):
        """Test extracting empty CSV."""
        filepath = tmp_path / "empty.csv"
        filepath.write_text("")
        extractor = CSVExtractor(filepath)
        records = extractor.extract()
        assert records == []


class TestInMemoryExtractor:
    """Tests for InMemoryExtractor."""

    def test_extract_returns_copy(self, sample_records):
        """Test that extract returns a copy."""
        extractor = InMemoryExtractor(sample_records)
        records = extractor.extract()
        assert records == sample_records
        assert records is not sample_records  # Should be a copy


# =============================================================================
# Transformer Tests
# =============================================================================


class TestTransformer:
    """Tests for Transformer class."""

    def test_empty_transformer(self, sample_records):
        """Test transformer with no transformations."""
        transformer = Transformer()
        result = transformer.transform(sample_records)
        assert result == sample_records

    def test_chain_transformations(self, sample_records):
        """Test chaining multiple transformations."""
        transformer = (
            Transformer()
            .add(lowercase_keys)
            .add(clean_whitespace)
        )
        result = transformer.transform(sample_records)
        assert "name" in result[0]
        assert "Name" not in result[0]


class TestTransformFunctions:
    """Tests for transformation functions."""

    def test_clean_whitespace(self):
        """Test whitespace cleaning."""
        record = {"name": "  Alice  ", "city": "NYC"}
        result = clean_whitespace(record)
        assert result["name"] == "Alice"
        assert result["city"] == "NYC"

    def test_lowercase_keys(self):
        """Test lowercase key conversion."""
        record = {"Name": "Alice", "AGE": 25}
        result = lowercase_keys(record)
        assert "name" in result
        assert "age" in result

    def test_rename_fields(self):
        """Test field renaming."""
        record = {"old_name": "value"}
        rename = rename_fields({"old_name": "new_name"})
        result = rename(record)
        assert "new_name" in result
        assert "old_name" not in result

    def test_filter_fields(self):
        """Test field filtering."""
        record = {"name": "Alice", "age": 25, "city": "NYC"}
        filter_fn = filter_fields(["name", "age"])
        result = filter_fn(record)
        assert set(result.keys()) == {"name", "age"}

    def test_add_timestamp(self):
        """Test timestamp addition."""
        record = {"name": "Alice"}
        add_ts = add_timestamp("created_at")
        result = add_ts(record)
        assert "created_at" in result

    def test_convert_types_int(self):
        """Test integer type conversion."""
        record = {"age": "25", "name": "Alice"}
        convert = convert_types({"age": int})
        result = convert(record)
        assert result["age"] == 25
        assert isinstance(result["age"], int)

    def test_convert_types_float(self):
        """Test float type conversion."""
        record = {"price": "19.99"}
        convert = convert_types({"price": float})
        result = convert(record)
        assert result["price"] == 19.99

    def test_convert_types_bool(self):
        """Test boolean type conversion."""
        record = {"active": "true", "enabled": "1", "disabled": "false"}
        convert = convert_types({"active": bool, "enabled": bool, "disabled": bool})
        result = convert(record)
        assert result["active"] is True
        assert result["enabled"] is True
        assert result["disabled"] is False

    def test_filter_records(self):
        """Test record filtering."""
        records = [
            {"name": "Alice", "age": 25},
            {"name": "Bob", "age": 17},
            {"name": "Carol", "age": 30},
        ]
        transformer = Transformer().add(
            filter_records(lambda r: r["age"] >= 18)
        )
        result = transformer.transform(records)
        assert len(result) == 2
        assert all(r["age"] >= 18 for r in result)

    def test_validate_required(self):
        """Test required field validation."""
        records = [
            {"name": "Alice", "email": "alice@example.com"},
            {"name": "Bob", "email": ""},
            {"name": "Carol"},
        ]
        transformer = Transformer().add(validate_required(["name", "email"]))
        result = transformer.transform(records)
        assert len(result) == 1
        assert result[0]["name"] == "Alice"

    def test_compute_field(self):
        """Test computed field."""
        record = {"price": 100, "quantity": 5}
        compute = compute_field("total", lambda r: r["price"] * r["quantity"])
        result = compute(record)
        assert result["total"] == 500


# =============================================================================
# Loader Tests
# =============================================================================


class TestJSONLoader:
    """Tests for JSONLoader."""

    def test_load_json(self, tmp_path, sample_records):
        """Test loading to JSON file."""
        filepath = tmp_path / "output.json"
        loader = JSONLoader(filepath)
        count = loader.load(sample_records)

        assert count == 3
        assert filepath.exists()

        with open(filepath) as f:
            loaded = json.load(f)
        assert len(loaded) == 3

    def test_load_creates_directory(self, tmp_path, sample_records):
        """Test that loader creates parent directories."""
        filepath = tmp_path / "nested" / "dir" / "output.json"
        loader = JSONLoader(filepath)
        loader.load(sample_records)
        assert filepath.exists()


class TestJSONLLoader:
    """Tests for JSONLLoader."""

    def test_load_jsonl(self, tmp_path, sample_records):
        """Test loading to JSONL file."""
        filepath = tmp_path / "output.jsonl"
        loader = JSONLLoader(filepath)
        count = loader.load(sample_records)

        assert count == 3
        assert filepath.exists()

        with open(filepath) as f:
            lines = f.readlines()
        assert len(lines) == 3

        # Each line should be valid JSON
        for line in lines:
            json.loads(line)


class TestCSVLoader:
    """Tests for CSVLoader."""

    def test_load_csv(self, tmp_path, sample_records):
        """Test loading to CSV file."""
        filepath = tmp_path / "output.csv"
        loader = CSVLoader(filepath)
        count = loader.load(sample_records)

        assert count == 3
        assert filepath.exists()

        content = filepath.read_text()
        lines = content.strip().split("\n")
        assert len(lines) == 4  # Header + 3 records

    def test_load_empty_csv(self, tmp_path):
        """Test loading empty records to CSV."""
        filepath = tmp_path / "empty.csv"
        loader = CSVLoader(filepath)
        count = loader.load([])
        assert count == 0


class TestInMemoryLoader:
    """Tests for InMemoryLoader."""

    def test_load_and_retrieve(self, sample_records):
        """Test loading and retrieving data."""
        loader = InMemoryLoader()
        count = loader.load(sample_records)

        assert count == 3
        assert loader.get_data() == sample_records

    def test_clear(self, sample_records):
        """Test clearing loaded data."""
        loader = InMemoryLoader()
        loader.load(sample_records)
        loader.clear()
        assert loader.get_data() == []


# =============================================================================
# Pipeline Tests
# =============================================================================


class TestPipelineStats:
    """Tests for PipelineStats."""

    def test_success_rate_all_success(self):
        """Test success rate with no failures."""
        stats = PipelineStats(
            records_extracted=100,
            records_loaded=100,
            records_failed=0
        )
        assert stats.success_rate == 100.0

    def test_success_rate_partial(self):
        """Test success rate with some failures."""
        stats = PipelineStats(
            records_extracted=100,
            records_failed=25
        )
        assert stats.success_rate == 75.0

    def test_success_rate_empty(self):
        """Test success rate with no records."""
        stats = PipelineStats()
        assert stats.success_rate == 100.0

    def test_to_dict(self):
        """Test stats to dictionary conversion."""
        stats = PipelineStats(
            records_extracted=100,
            records_transformed=90,
            records_loaded=90,
            records_failed=10
        )
        result = stats.to_dict()
        assert result["records_extracted"] == 100
        assert result["success_rate"] == 90.0


class TestETLPipeline:
    """Tests for ETLPipeline."""

    def test_basic_pipeline(self, sample_records):
        """Test basic pipeline execution."""
        extractor = InMemoryExtractor(sample_records)
        loader = InMemoryLoader()

        pipeline = (
            ETLPipeline()
            .extract_from(extractor)
            .load_to(loader)
        )

        stats = pipeline.run()

        assert stats.records_extracted == 3
        assert stats.records_loaded == 3
        assert loader.get_data() == sample_records

    def test_pipeline_with_transformer(self, sample_records):
        """Test pipeline with transformations."""
        extractor = InMemoryExtractor(sample_records)
        transformer = Transformer().add(lowercase_keys)
        loader = InMemoryLoader()

        pipeline = (
            ETLPipeline()
            .extract_from(extractor)
            .transform_with(transformer)
            .load_to(loader)
        )

        stats = pipeline.run()

        assert stats.records_extracted == 3
        assert stats.records_transformed == 3
        assert "name" in loader.get_data()[0]

    def test_pipeline_no_extractor(self):
        """Test pipeline without extractor raises error."""
        pipeline = ETLPipeline().load_to(InMemoryLoader())
        with pytest.raises(ValueError, match="No extractor"):
            pipeline.run()

    def test_pipeline_no_loader(self, sample_records):
        """Test pipeline without loader raises error."""
        pipeline = ETLPipeline().extract_from(InMemoryExtractor(sample_records))
        with pytest.raises(ValueError, match="No loader"):
            pipeline.run()

    def test_pipeline_with_config(self, sample_records):
        """Test pipeline with custom config."""
        config = PipelineConfig(
            name="test-pipeline",
            batch_size=500,
            fail_on_error=True
        )

        pipeline = (
            ETLPipeline(config)
            .extract_from(InMemoryExtractor(sample_records))
            .load_to(InMemoryLoader())
        )

        assert pipeline.config.name == "test-pipeline"
        assert pipeline.config.batch_size == 500


class TestEndToEndPipelines:
    """End-to-end pipeline tests."""

    def test_json_to_json_pipeline(self, sample_json_file, tmp_path):
        """Test JSON to JSON pipeline."""
        output_file = tmp_path / "output.json"

        transformer = (
            Transformer()
            .add(lowercase_keys)
            .add(convert_types({"age": int}))
        )

        pipeline = (
            ETLPipeline(PipelineConfig(name="json-to-json"))
            .extract_from(JSONExtractor(sample_json_file))
            .transform_with(transformer)
            .load_to(JSONLoader(output_file))
        )

        stats = pipeline.run()

        assert stats.records_loaded == 3
        assert output_file.exists()

        with open(output_file) as f:
            result = json.load(f)
        assert result[0]["age"] == 25

    def test_csv_to_jsonl_pipeline(self, sample_csv_file, tmp_path):
        """Test CSV to JSONL pipeline."""
        output_file = tmp_path / "output.jsonl"

        transformer = (
            Transformer()
            .add(lowercase_keys)
            .add(add_timestamp())
        )

        pipeline = (
            ETLPipeline(PipelineConfig(name="csv-to-jsonl"))
            .extract_from(CSVExtractor(sample_csv_file))
            .transform_with(transformer)
            .load_to(JSONLLoader(output_file))
        )

        stats = pipeline.run()

        assert stats.records_loaded == 3

        with open(output_file) as f:
            lines = f.readlines()
        assert len(lines) == 3

        first_record = json.loads(lines[0])
        assert "processed_at" in first_record

    def test_filtering_pipeline(self):
        """Test pipeline with filtering."""
        records = [
            {"name": "Alice", "score": 85},
            {"name": "Bob", "score": 45},
            {"name": "Carol", "score": 92},
            {"name": "David", "score": 60},
        ]

        transformer = (
            Transformer()
            .add(filter_records(lambda r: r["score"] >= 60))
        )

        loader = InMemoryLoader()

        pipeline = (
            ETLPipeline()
            .extract_from(InMemoryExtractor(records))
            .transform_with(transformer)
            .load_to(loader)
        )

        stats = pipeline.run()

        assert stats.records_extracted == 4
        assert stats.records_loaded == 3  # Bob filtered out
        assert all(r["score"] >= 60 for r in loader.get_data())
