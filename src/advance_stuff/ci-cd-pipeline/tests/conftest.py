"""
Pytest Configuration and Fixtures

Common fixtures and configuration for all tests.
"""

import pytest
from fastapi.testclient import TestClient

from myapp.api import app


@pytest.fixture
def client() -> TestClient:
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def sample_data() -> dict:
    """Provide sample test data."""
    return {
        "name": "Test User",
        "values": [1, 2, 3, 4, 5],
        "metadata": {"created": "2024-01-01"},
    }


@pytest.fixture
def empty_data() -> dict:
    """Provide empty test data."""
    return {}


@pytest.fixture
def numbers() -> list[int]:
    """Provide a list of numbers for testing."""
    return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
