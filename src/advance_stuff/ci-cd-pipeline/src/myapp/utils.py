"""
MyApp - Utility Functions

Common utility functions used throughout the application.
"""

import hashlib
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any


def get_env(key: str, default: str = "") -> str:
    """Get an environment variable with a default value.

    Args:
        key: The environment variable name.
        default: Default value if not set.

    Returns:
        The environment variable value or default.
    """
    return os.getenv(key, default)


def get_timestamp() -> str:
    """Get current timestamp in ISO format.

    Returns:
        Current timestamp as ISO format string.
    """
    return datetime.now().isoformat()


def hash_string(value: str) -> str:
    """Generate SHA256 hash of a string.

    Args:
        value: String to hash.

    Returns:
        Hexadecimal hash string.
    """
    return hashlib.sha256(value.encode()).hexdigest()


def load_json(filepath: str | Path) -> dict[str, Any]:
    """Load JSON from a file.

    Args:
        filepath: Path to JSON file.

    Returns:
        Parsed JSON as dictionary.

    Raises:
        FileNotFoundError: If file doesn't exist.
        json.JSONDecodeError: If JSON is invalid.
    """
    with open(filepath) as f:
        return json.load(f)


def save_json(data: dict[str, Any], filepath: str | Path, indent: int = 2) -> None:
    """Save data to a JSON file.

    Args:
        data: Data to save.
        filepath: Output file path.
        indent: JSON indentation level.
    """
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=indent)


def ensure_dir(path: str | Path) -> Path:
    """Ensure a directory exists, creating it if necessary.

    Args:
        path: Directory path.

    Returns:
        Path object for the directory.
    """
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def chunk_list(items: list[Any], size: int) -> list[list[Any]]:
    """Split a list into chunks of specified size.

    Args:
        items: List to split.
        size: Maximum chunk size.

    Returns:
        List of chunks.
    """
    return [items[i : i + size] for i in range(0, len(items), size)]


def flatten_dict(
    d: dict[str, Any], parent_key: str = "", sep: str = "."
) -> dict[str, Any]:
    """Flatten a nested dictionary.

    Args:
        d: Dictionary to flatten.
        parent_key: Parent key prefix.
        sep: Separator between keys.

    Returns:
        Flattened dictionary.

    Example:
        >>> flatten_dict({"a": {"b": 1, "c": 2}})
        {"a.b": 1, "a.c": 2}
    """
    items: list[tuple[str, Any]] = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
