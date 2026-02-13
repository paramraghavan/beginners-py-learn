"""
MyApp - Sample Python Application

This module provides the main entry point and core functionality.
"""

import sys
from dataclasses import dataclass


@dataclass
class AppConfig:
    """Application configuration."""

    name: str = "MyApp"
    version: str = "0.1.0"
    debug: bool = False


def get_version() -> str:
    """Return the application version."""
    return AppConfig().version


def greet(name: str) -> str:
    """Generate a greeting message.

    Args:
        name: The name to greet.

    Returns:
        A greeting string.
    """
    if not name:
        raise ValueError("Name cannot be empty")
    return f"Hello, {name}! Welcome to MyApp."


def calculate_sum(numbers: list[int | float]) -> float:
    """Calculate the sum of a list of numbers.

    Args:
        numbers: List of numbers to sum.

    Returns:
        The sum of all numbers.

    Raises:
        ValueError: If the list is empty.
    """
    if not numbers:
        raise ValueError("Cannot calculate sum of empty list")
    return sum(numbers)


def process_data(data: dict) -> dict:
    """Process input data and return results.

    Args:
        data: Input data dictionary.

    Returns:
        Processed data with additional fields.
    """
    result = {
        "input": data,
        "processed": True,
        "item_count": len(data),
    }

    # Add computed fields
    if "values" in data and isinstance(data["values"], list):
        result["total"] = calculate_sum(data["values"])

    return result


def main() -> int:
    """Main entry point for the application."""
    config = AppConfig()
    print(f"{config.name} v{config.version}")
    print(greet("World"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
