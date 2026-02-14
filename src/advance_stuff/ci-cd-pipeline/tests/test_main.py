"""
Tests for myapp.main module
"""

import pytest

from myapp.main import (
    AppConfig,
    calculate_sum,
    get_version,
    greet,
    main,
    process_data,
)


class TestAppConfig:
    """Tests for AppConfig dataclass."""

    def test_default_values(self):
        """Test default configuration values."""
        config = AppConfig()
        assert config.name == "MyApp"
        assert config.version == "0.1.0"
        assert config.debug is False

    def test_custom_values(self):
        """Test custom configuration values."""
        config = AppConfig(name="CustomApp", version="1.0.0", debug=True)
        assert config.name == "CustomApp"
        assert config.version == "1.0.0"
        assert config.debug is True


class TestGetVersion:
    """Tests for get_version function."""

    def test_returns_version_string(self):
        """Test that get_version returns the version string."""
        version = get_version()
        assert isinstance(version, str)
        assert version == "0.1.0"


class TestGreet:
    """Tests for greet function."""

    def test_greet_with_name(self):
        """Test greeting with a valid name."""
        result = greet("Alice")
        assert result == "Hello, Alice! Welcome to MyApp."

    def test_greet_with_different_names(self):
        """Test greeting with various names."""
        names = ["Bob", "Charlie", "Diana"]
        for name in names:
            result = greet(name)
            assert name in result
            assert "Hello" in result
            assert "Welcome" in result

    def test_greet_with_empty_name_raises_error(self):
        """Test that empty name raises ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            greet("")


class TestCalculateSum:
    """Tests for calculate_sum function."""

    def test_sum_integers(self, numbers):
        """Test sum of integers."""
        result = calculate_sum(numbers)
        assert result == 55

    def test_sum_floats(self):
        """Test sum of floats."""
        result = calculate_sum([1.5, 2.5, 3.0])
        assert result == 7.0

    def test_sum_mixed(self):
        """Test sum of mixed integers and floats."""
        result = calculate_sum([1, 2.5, 3, 4.5])
        assert result == 11.0

    def test_sum_single_element(self):
        """Test sum of single element."""
        result = calculate_sum([42])
        assert result == 42

    def test_sum_negative_numbers(self):
        """Test sum with negative numbers."""
        result = calculate_sum([-1, -2, 3, 4])
        assert result == 4

    def test_sum_empty_list_raises_error(self):
        """Test that empty list raises ValueError."""
        with pytest.raises(ValueError, match="empty list"):
            calculate_sum([])


class TestProcessData:
    """Tests for process_data function."""

    def test_process_basic_data(self, sample_data):
        """Test processing basic data."""
        result = process_data(sample_data)
        assert result["processed"] is True
        assert result["item_count"] == 3
        assert result["input"] == sample_data

    def test_process_with_values(self, sample_data):
        """Test processing data with values calculates total."""
        result = process_data(sample_data)
        assert result["total"] == 15  # 1+2+3+4+5

    def test_process_empty_data(self, empty_data):
        """Test processing empty data."""
        result = process_data(empty_data)
        assert result["processed"] is True
        assert result["item_count"] == 0
        assert "total" not in result

    def test_process_data_without_values(self):
        """Test processing data without values key."""
        data = {"key": "value"}
        result = process_data(data)
        assert result["processed"] is True
        assert "total" not in result


class TestMain:
    """Tests for main function."""

    def test_main_returns_zero(self):
        """Test that main returns 0 on success."""
        result = main()
        assert result == 0

    def test_main_output(self, capsys):
        """Test main function output."""
        main()
        captured = capsys.readouterr()
        assert "MyApp" in captured.out
        assert "Hello, World!" in captured.out
