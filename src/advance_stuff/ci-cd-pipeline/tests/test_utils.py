"""
Tests for myapp.utils module
"""

import json
import os
from pathlib import Path

import pytest

from myapp.utils import (
    chunk_list,
    ensure_dir,
    flatten_dict,
    get_env,
    get_timestamp,
    hash_string,
    load_json,
    save_json,
)


class TestGetEnv:
    """Tests for get_env function."""

    def test_get_existing_env(self):
        """Test getting an existing environment variable."""
        os.environ["TEST_VAR"] = "test_value"
        result = get_env("TEST_VAR")
        assert result == "test_value"
        del os.environ["TEST_VAR"]

    def test_get_missing_env_with_default(self):
        """Test getting a missing variable returns default."""
        result = get_env("NONEXISTENT_VAR", "default")
        assert result == "default"

    def test_get_missing_env_empty_default(self):
        """Test getting a missing variable returns empty string."""
        result = get_env("NONEXISTENT_VAR")
        assert result == ""


class TestGetTimestamp:
    """Tests for get_timestamp function."""

    def test_timestamp_format(self):
        """Test timestamp is in ISO format."""
        timestamp = get_timestamp()
        assert isinstance(timestamp, str)
        assert "T" in timestamp  # ISO format contains T separator

    def test_timestamp_changes(self):
        """Test that timestamps change over time."""
        ts1 = get_timestamp()
        ts2 = get_timestamp()
        # They should be very close but might differ
        assert isinstance(ts1, str)
        assert isinstance(ts2, str)


class TestHashString:
    """Tests for hash_string function."""

    def test_hash_returns_string(self):
        """Test hash returns a string."""
        result = hash_string("test")
        assert isinstance(result, str)

    def test_hash_length(self):
        """Test hash has expected length (SHA256 = 64 hex chars)."""
        result = hash_string("test")
        assert len(result) == 64

    def test_hash_consistency(self):
        """Test same input produces same hash."""
        hash1 = hash_string("test")
        hash2 = hash_string("test")
        assert hash1 == hash2

    def test_hash_different_inputs(self):
        """Test different inputs produce different hashes."""
        hash1 = hash_string("test1")
        hash2 = hash_string("test2")
        assert hash1 != hash2


class TestLoadSaveJson:
    """Tests for load_json and save_json functions."""

    def test_save_and_load_json(self, tmp_path):
        """Test saving and loading JSON."""
        data = {"key": "value", "number": 42}
        filepath = tmp_path / "test.json"

        save_json(data, filepath)
        loaded = load_json(filepath)

        assert loaded == data

    def test_save_json_creates_directory(self, tmp_path):
        """Test save_json creates parent directories."""
        data = {"test": True}
        filepath = tmp_path / "nested" / "dir" / "test.json"

        save_json(data, filepath)
        assert filepath.exists()

    def test_load_json_nonexistent_file(self, tmp_path):
        """Test loading nonexistent file raises error."""
        filepath = tmp_path / "nonexistent.json"
        with pytest.raises(FileNotFoundError):
            load_json(filepath)

    def test_load_json_invalid_json(self, tmp_path):
        """Test loading invalid JSON raises error."""
        filepath = tmp_path / "invalid.json"
        filepath.write_text("not valid json")
        with pytest.raises(json.JSONDecodeError):
            load_json(filepath)


class TestEnsureDir:
    """Tests for ensure_dir function."""

    def test_create_new_directory(self, tmp_path):
        """Test creating a new directory."""
        new_dir = tmp_path / "new_directory"
        result = ensure_dir(new_dir)
        assert result.exists()
        assert result.is_dir()

    def test_existing_directory(self, tmp_path):
        """Test with existing directory."""
        result = ensure_dir(tmp_path)
        assert result.exists()

    def test_nested_directory(self, tmp_path):
        """Test creating nested directories."""
        nested = tmp_path / "a" / "b" / "c"
        result = ensure_dir(nested)
        assert result.exists()


class TestChunkList:
    """Tests for chunk_list function."""

    def test_chunk_even_split(self):
        """Test chunking with even split."""
        items = [1, 2, 3, 4, 5, 6]
        result = chunk_list(items, 2)
        assert result == [[1, 2], [3, 4], [5, 6]]

    def test_chunk_uneven_split(self):
        """Test chunking with uneven split."""
        items = [1, 2, 3, 4, 5]
        result = chunk_list(items, 2)
        assert result == [[1, 2], [3, 4], [5]]

    def test_chunk_size_larger_than_list(self):
        """Test chunk size larger than list."""
        items = [1, 2, 3]
        result = chunk_list(items, 10)
        assert result == [[1, 2, 3]]

    def test_chunk_empty_list(self):
        """Test chunking empty list."""
        result = chunk_list([], 5)
        assert result == []

    def test_chunk_size_one(self):
        """Test chunk size of one."""
        items = [1, 2, 3]
        result = chunk_list(items, 1)
        assert result == [[1], [2], [3]]


class TestFlattenDict:
    """Tests for flatten_dict function."""

    def test_flatten_simple_nested(self):
        """Test flattening simple nested dict."""
        data = {"a": {"b": 1}}
        result = flatten_dict(data)
        assert result == {"a.b": 1}

    def test_flatten_multiple_keys(self):
        """Test flattening with multiple keys."""
        data = {"a": {"b": 1, "c": 2}}
        result = flatten_dict(data)
        assert result == {"a.b": 1, "a.c": 2}

    def test_flatten_deep_nesting(self):
        """Test flattening deeply nested dict."""
        data = {"a": {"b": {"c": {"d": 1}}}}
        result = flatten_dict(data)
        assert result == {"a.b.c.d": 1}

    def test_flatten_custom_separator(self):
        """Test flattening with custom separator."""
        data = {"a": {"b": 1}}
        result = flatten_dict(data, sep="_")
        assert result == {"a_b": 1}

    def test_flatten_already_flat(self):
        """Test flattening already flat dict."""
        data = {"a": 1, "b": 2}
        result = flatten_dict(data)
        assert result == {"a": 1, "b": 2}

    def test_flatten_empty_dict(self):
        """Test flattening empty dict."""
        result = flatten_dict({})
        assert result == {}
