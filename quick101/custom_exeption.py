"""
# Inherit from Exception (or a more specific exception type)
# Use pass for simple exceptions that don't need custom behavior
# Override __init__() to accept custom parameters
# Call super().__init__() to properly initialize the base exception
# Override __str__() for better error messages
"""


# Basic custom exception
class CustomError(Exception):
    """A simple custom exception"""
    pass


# Custom exception with custom message
class ValidationError(Exception):
    """Raised when validation fails"""

    def __init__(self, message="Validation failed"):
        self.message = message
        super().__init__(self.message)


# More advanced custom exception with additional attributes
class DatabaseError(Exception):
    """Custom exception for database operations"""

    def __init__(self, message, error_code=None, query=None):
        self.message = message
        self.error_code = error_code
        self.query = query
        super().__init__(self.message)

    def __str__(self):
        if self.error_code:
            return f"DatabaseError [{self.error_code}]: {self.message}"
        return f"DatabaseError: {self.message}"


# Custom exception with multiple inheritance (less common)
class NetworkTimeoutError(Exception, TimeoutError):
    """Raised when network operations timeout"""

    def __init__(self, message, timeout_duration=None):
        self.timeout_duration = timeout_duration
        super().__init__(message)


# Example usage
def validate_age(age):
    if age < 0:
        raise ValidationError("Age cannot be negative")
    if age > 150:
        raise ValidationError("Age seems unrealistic")
    return True


def connect_to_database(connection_string):
    if not connection_string:
        raise DatabaseError("Connection string is required", error_code="DB001")
    # Simulate connection logic
    if "invalid" in connection_string:
        raise DatabaseError(
            "Failed to connect to database",
            error_code="DB002",
            query=connection_string
        )


# Using the custom exceptions
if __name__ == "__main__":
    # Example 1: Basic custom exception
    try:
        raise CustomError("Something went wrong!")
    except CustomError as e:
        print(f"Caught custom error: {e}")

    # Example 2: Validation error
    try:
        validate_age(-5)
    except ValidationError as e:
        print(f"Validation failed: {e.message}")

    # Example 3: Database error with additional info
    try:
        connect_to_database("invalid_connection")
    except DatabaseError as e:
        print(f"Database error: {e}")
        print(f"Error code: {e.error_code}")
        print(f"Query: {e.query}")

    # Example 4: Catching multiple exception types
    try:
        # This could raise either ValidationError or DatabaseError
        validate_age(25)
        connect_to_database("")
    except (ValidationError, DatabaseError) as e:
        print(f"Operation failed: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


# Best practices for custom exceptions:

# 1. Create a hierarchy for related exceptions
class AppError(Exception):
    """Base exception for application errors"""
    pass


class UserError(AppError):
    """Errors related to user operations"""
    pass


class SystemError(AppError):
    """Errors related to system operations"""
    pass


class AuthenticationError(UserError):
    """Authentication failed"""
    pass


class AuthorizationError(UserError):
    """User not authorized"""
    pass


# 2. Add helpful context and methods
class APIError(Exception):
    """Exception for API-related errors"""

    def __init__(self, message, status_code=None, response_data=None):
        self.message = message
        self.status_code = status_code
        self.response_data = response_data
        super().__init__(self.message)

    @property
    def is_client_error(self):
        return self.status_code and 400 <= self.status_code < 500

    @property
    def is_server_error(self):
        return self.status_code and 500 <= self.status_code < 600