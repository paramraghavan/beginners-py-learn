"""Tests for calculator module"""

import pytest
from src.calculator import add, subtract, multiply, divide, power, absolute


class TestAddition:
    """Tests for add function"""

    def test_add_positive_numbers(self):
        """Test adding two positive numbers"""
        assert add(2, 3) == 5

    def test_add_negative_numbers(self):
        """Test adding two negative numbers"""
        assert add(-2, -3) == -5

    def test_add_zero(self):
        """Test adding with zero"""
        assert add(0, 5) == 5


class TestSubtraction:
    """Tests for subtract function"""

    def test_subtract_positive_numbers(self):
        """Test subtracting positive numbers"""
        assert subtract(5, 3) == 2

    def test_subtract_negative_result(self):
        """Test subtraction resulting in negative"""
        assert subtract(2, 5) == -3


class TestMultiplication:
    """Tests for multiply function"""

    def test_multiply_positive_numbers(self):
        """Test multiplying positive numbers"""
        assert multiply(3, 4) == 12

    def test_multiply_by_zero(self):
        """Test multiplying by zero"""
        assert multiply(5, 0) == 0


class TestDivision:
    """Tests for divide function"""

    def test_divide_positive_numbers(self):
        """Test dividing positive numbers"""
        assert divide(10, 2) == 5

    def test_divide_negative_numbers(self):
        """Test dividing negative numbers"""
        assert divide(-10, 2) == -5

    def test_divide_by_zero_raises_error(self):
        """Test that dividing by zero raises ValueError"""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(10, 0)

    def test_divide_returns_float(self):
        """Test that divide returns float"""
        result = divide(5, 2)
        assert isinstance(result, float)
        assert result == 2.5


class TestPower:
    """Tests for power function"""

    def test_power_positive_exponent(self):
        """Test power with positive exponent"""
        assert power(2, 3) == 8

    def test_power_zero_exponent(self):
        """Test power with zero exponent"""
        assert power(5, 0) == 1

    def test_power_negative_exponent_raises_error(self):
        """Test that negative exponent raises ValueError"""
        with pytest.raises(ValueError, match="Exponent must be non-negative"):
            power(2, -1)


class TestAbsolute:
    """Tests for absolute function"""

    def test_absolute_positive_number(self):
        """Test absolute value of positive number"""
        assert absolute(5) == 5

    def test_absolute_negative_number(self):
        """Test absolute value of negative number"""
        assert absolute(-5) == 5

    def test_absolute_zero(self):
        """Test absolute value of zero"""
        assert absolute(0) == 0


# NOTE: We're intentionally not testing all edge cases
# This will show low coverage when we run the tool
