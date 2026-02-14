"""
Tests for myapp.api module
"""

import pytest


class TestRootEndpoint:
    """Tests for the root endpoint."""

    def test_root_returns_ok(self, client):
        """Test root endpoint returns status ok."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "version" in data

    def test_root_returns_version(self, client):
        """Test root endpoint includes version."""
        response = client.get("/")
        data = response.json()
        assert data["version"] == "0.1.0"


class TestHealthEndpoint:
    """Tests for the health check endpoint."""

    def test_health_returns_healthy(self, client):
        """Test health check returns healthy status."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestGreetEndpoint:
    """Tests for the greet endpoint."""

    def test_greet_success(self, client):
        """Test successful greeting."""
        response = client.post("/greet", json={"name": "Alice"})
        assert response.status_code == 200
        data = response.json()
        assert "Hello, Alice!" in data["message"]

    def test_greet_different_names(self, client):
        """Test greeting with different names."""
        names = ["Bob", "Charlie", "Diana"]
        for name in names:
            response = client.post("/greet", json={"name": name})
            assert response.status_code == 200
            assert name in response.json()["message"]

    def test_greet_empty_name_fails(self, client):
        """Test that empty name returns 422."""
        response = client.post("/greet", json={"name": ""})
        assert response.status_code == 422

    def test_greet_missing_name_fails(self, client):
        """Test that missing name returns 422."""
        response = client.post("/greet", json={})
        assert response.status_code == 422


class TestSumEndpoint:
    """Tests for the sum endpoint."""

    def test_sum_integers(self, client):
        """Test sum of integers."""
        response = client.post("/sum", json={"numbers": [1, 2, 3, 4, 5]})
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 15
        assert data["count"] == 5

    def test_sum_floats(self, client):
        """Test sum of floats."""
        response = client.post("/sum", json={"numbers": [1.5, 2.5, 3.0]})
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 7.0

    def test_sum_single_number(self, client):
        """Test sum of single number."""
        response = client.post("/sum", json={"numbers": [42]})
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 42
        assert data["count"] == 1

    def test_sum_empty_list_fails(self, client):
        """Test that empty list returns 422."""
        response = client.post("/sum", json={"numbers": []})
        assert response.status_code == 422


class TestProcessEndpoint:
    """Tests for the process endpoint."""

    def test_process_basic_data(self, client, sample_data):
        """Test processing basic data."""
        response = client.post("/process", json={"data": sample_data})
        assert response.status_code == 200
        data = response.json()
        assert data["processed"] is True
        assert data["item_count"] == 3

    def test_process_with_values(self, client):
        """Test processing data with values."""
        response = client.post(
            "/process", json={"data": {"values": [1, 2, 3, 4, 5]}}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 15

    def test_process_empty_data(self, client, empty_data):
        """Test processing empty data."""
        response = client.post("/process", json={"data": empty_data})
        assert response.status_code == 200
        data = response.json()
        assert data["item_count"] == 0


class TestVersionEndpoint:
    """Tests for the version endpoint."""

    def test_version_returns_info(self, client):
        """Test version endpoint returns app info."""
        response = client.get("/version")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "MyApp"
        assert data["version"] == "0.1.0"


class TestAPIDocumentation:
    """Tests for API documentation endpoints."""

    def test_openapi_schema(self, client):
        """Test OpenAPI schema is available."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "paths" in data
        assert "info" in data

    def test_docs_redirect(self, client):
        """Test docs endpoint is available."""
        response = client.get("/docs")
        assert response.status_code == 200
