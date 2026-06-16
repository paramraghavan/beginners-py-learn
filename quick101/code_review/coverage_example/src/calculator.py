"""Calculator module with various operations"""


def add(a, b):
    """Add two numbers

    Args:
        a: First number
        b: Second number

    Returns:
        Sum of a and b
    """
    return a + b


def subtract(a, b):
    """Subtract two numbers

    Args:
        a: First number
        b: Second number

    Returns:
        Difference of a and b
    """
    return a - b


def multiply(a, b):
    """Multiply two numbers

    Args:
        a: First number
        b: Second number

    Returns:
        Product of a and b
    """
    return a * b


def divide(a, b):
    """Divide two numbers

    Args:
        a: Dividend
        b: Divisor

    Returns:
        Result of a / b

    Raises:
        ValueError: If b is zero
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def power(base, exponent):
    """Calculate base raised to exponent

    Args:
        base: Base number
        exponent: Exponent

    Returns:
        base ** exponent
    """
    if exponent < 0:
        raise ValueError("Exponent must be non-negative")
    return base ** exponent


def absolute(a):
    """Get absolute value of a number

    Args:
        a: Any number

    Returns:
        Absolute value of a
    """
    if a < 0:
        return -a
    return a
