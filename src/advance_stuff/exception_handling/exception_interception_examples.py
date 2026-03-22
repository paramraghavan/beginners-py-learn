"""
Exception Interception Examples

Demonstrates all exception interception techniques with runnable examples.
Each technique shows how to catch, track, and handle exceptions.
"""

import functools
import time
from typing import Dict, List, Any


# ============================================================================
# TECHNIQUE 1: Direct Try-Except
# ============================================================================

def technique_1_try_except():
    """Simple try-except at the call site."""
    print("\n" + "="*70)
    print("TECHNIQUE 1: Direct Try-Except")
    print("="*70)

    def risky_operation():
        raise ValueError("Something went wrong")

    # Catch at the call site
    try:
        risky_operation()
    except ValueError as e:
        print(f"✓ Caught: {e}")

    print("Execution continues after exception")


# ============================================================================
# TECHNIQUE 2: Wrapper Function
# ============================================================================

def technique_2_wrapper():
    """Wrapper function that catches exceptions."""
    print("\n" + "="*70)
    print("TECHNIQUE 2: Wrapper Function")
    print("="*70)

    def risky_operation():
        raise ValueError("Database connection failed")

    def safe_wrapper(func, *args, **kwargs):
        """Wrapper that catches exceptions."""
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            print(f"✓ Caught: {e}")
            return None
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
            raise

    # Call through wrapper
    result = safe_wrapper(risky_operation)
    print(f"Result: {result}")
    print("Execution continues")


# ============================================================================
# TECHNIQUE 3: Decorator
# ============================================================================

def technique_3_decorator():
    """Decorator that intercepts function exceptions."""
    print("\n" + "="*70)
    print("TECHNIQUE 3: Decorator")
    print("="*70)

    def catches_exceptions(func):
        """Decorator that catches exceptions from a function."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValueError as e:
                print(f"✓ Caught: {e}")
                return None
            except Exception as e:
                raise
        return wrapper

    @catches_exceptions
    def my_operation():
        raise ValueError("Operation failed")

    @catches_exceptions
    def successful_operation():
        return "Success!"

    # Decorated functions have automatic error handling
    result1 = my_operation()  # Exception caught and suppressed
    print(f"Result 1: {result1}")

    result2 = successful_operation()  # Normal execution
    print(f"Result 2: {result2}")


# ============================================================================
# TECHNIQUE 4: Context Manager
# ============================================================================

def technique_4_context_manager():
    """Context manager that intercepts exceptions in a block."""
    print("\n" + "="*70)
    print("TECHNIQUE 4: Context Manager")
    print("="*70)

    class ExceptionTracker:
        """Context manager that tracks exceptions."""

        def __init__(self, name="Operation"):
            self.name = name
            self.exception_caught = None

        def __enter__(self):
            print(f"Starting: {self.name}")
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            if exc_type is not None:
                self.exception_caught = exc_value
                print(f"✓ Caught exception: {exc_type.__name__}: {exc_value}")
                # Return True to suppress, False to propagate
                return True
            else:
                print(f"Completed: {self.name}")
            return False

    # Usage 1: Exception is caught and suppressed
    with ExceptionTracker("Database operation") as tracker:
        raise ValueError("Connection failed")

    print(f"Caught: {tracker.exception_caught}")

    # Usage 2: No exception
    with ExceptionTracker("File operation"):
        print("Reading file...")

    print("Execution continues")


# ============================================================================
# TECHNIQUE 5: Monkey Patching
# ============================================================================

def technique_5_monkey_patching():
    """Replace a function at runtime to intercept calls."""
    print("\n" + "="*70)
    print("TECHNIQUE 5: Monkey Patching")
    print("="*70)

    class DataHandler:
        def process(self, data):
            if not data:
                raise ValueError("No data provided")
            return f"Processed: {data}"

    # Save original
    handler = DataHandler()
    _original_process = handler.process

    # Create interceptor
    def intercepted_process(data):
        print(f"📍 Intercepted call with data: {data}")
        try:
            result = _original_process(data)
            print(f"✓ Success: {result}")
            return result
        except ValueError as e:
            print(f"✓ Caught: {e}")
            return f"Error handled: {e}"

    # Monkey patch
    handler.process = intercepted_process

    # Now all calls go through interceptor
    print("\nCall 1:")
    handler.process("test")

    print("\nCall 2:")
    handler.process(None)  # Will raise, but caught by interceptor


# ============================================================================
# TECHNIQUE 6: Class-level Monkey Patching
# ============================================================================

def technique_6_class_monkey_patching():
    """Monkey patch at the class level (like permission_analyzer_runtime)."""
    print("\n" + "="*70)
    print("TECHNIQUE 6: Class-Level Monkey Patching")
    print("="*70)

    class APIClient:
        def request(self, endpoint):
            if endpoint == "/forbidden":
                raise PermissionError("Access denied")
            return {"status": "ok", "data": "response"}

    # Save original method
    _original_request = APIClient.request

    # Create tracking data
    tracked_calls = []

    # Create interceptor
    def tracked_request(self, endpoint):
        try:
            return _original_request(self, endpoint)
        except PermissionError as e:
            tracked_calls.append({"endpoint": endpoint, "error": str(e)})
            print(f"✓ Permission error intercepted: {e}")
            return {"status": "error", "error": str(e)}

    # Monkey patch at class level
    APIClient.request = tracked_request

    # Now all instances use the patched method
    client = APIClient()

    print("\nRequest 1:")
    client.request("/data")

    print("\nRequest 2:")
    client.request("/forbidden")

    print(f"\nTracked errors: {tracked_calls}")


# ============================================================================
# ADVANCED: Combined Approach (Like permission_analyzer_runtime)
# ============================================================================

def advanced_combined_approach():
    """Combines monkey patching + context manager + exception tracking."""
    print("\n" + "="*70)
    print("ADVANCED: Combined Approach (Like permission_analyzer_runtime)")
    print("="*70)

    class AWSSimulator:
        """Simulates AWS API calls."""
        def call_api(self, service, operation):
            if operation == "AccessDenied":
                raise PermissionError(f"{service}:PermissionDenied")
            return f"Success: {service}.{operation}"

    class PermissionTracker:
        """Tracks permission errors like permission_analyzer_runtime."""

        def __init__(self):
            self.tracked_errors: Dict[str, List[str]] = {}
            self._original_method = None

        def __enter__(self):
            """Enter: Patch the AWS simulator."""
            self._patch()
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            """Exit: Restore original."""
            self._unpatch()
            return False

        def _patch(self):
            """Monkey patch the API call method."""
            self._original_method = AWSSimulator.call_api
            original_method = self._original_method  # Capture in closure
            tracked_errors = self.tracked_errors    # Capture tracker's error dict

            def tracked_call(aws_self, service, operation):
                try:
                    return original_method(aws_self, service, operation)
                except PermissionError as e:
                    # Track the error
                    if service not in tracked_errors:
                        tracked_errors[service] = []
                    tracked_errors[service].append(str(e))
                    print(f"✓ Permission error tracked: {e}")
                    # Return mock response
                    return f"Mock response (permission denied)"

            AWSSimulator.call_api = tracked_call

        def _unpatch(self):
            """Restore original method."""
            AWSSimulator.call_api = self._original_method

        def report(self):
            """Print tracking report."""
            print("\n📊 Permission Tracking Report:")
            if not self.tracked_errors:
                print("No permission errors")
            else:
                for service, errors in self.tracked_errors.items():
                    print(f"\n{service}:")
                    for error in errors:
                        print(f"  - {error}")

    # Usage
    aws = AWSSimulator()

    print("Normal usage (no tracking):")
    print(aws.call_api("s3", "PutObject"))

    print("\n\nWith PermissionTracker:")
    with PermissionTracker() as tracker:
        print(aws.call_api("s3", "GetObject"))
        print(aws.call_api("s3", "AccessDenied"))  # Error tracked
        print(aws.call_api("ec2", "AccessDenied"))  # Error tracked

    tracker.report()


# ============================================================================
# PRACTICAL EXAMPLE: Error Logging System
# ============================================================================

def practical_error_logging():
    """Practical example: Automatic error logging."""
    print("\n" + "="*70)
    print("PRACTICAL: Error Logging System")
    print("="*70)

    class ErrorLogger:
        """Logs all exceptions from decorated functions."""

        def __init__(self):
            self.errors: List[Dict[str, Any]] = []

        def track(self, func):
            """Decorator that logs exceptions."""
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    # Log the error
                    error_info = {
                        "function": func.__name__,
                        "exception_type": type(e).__name__,
                        "message": str(e),
                        "timestamp": time.time(),
                    }
                    self.errors.append(error_info)
                    print(f"✓ Error logged: {error_info['function']}: {error_info['message']}")
                    # Optionally re-raise or suppress
                    return None
            return wrapper

        def report(self):
            """Print error report."""
            print(f"\n📋 Error Report ({len(self.errors)} errors):")
            for i, error in enumerate(self.errors, 1):
                print(f"\n{i}. {error['function']}")
                print(f"   Type: {error['exception_type']}")
                print(f"   Message: {error['message']}")

    logger = ErrorLogger()

    @logger.track
    def database_query(table):
        if table == "invalid":
            raise ValueError("Table not found")
        return f"Query {table}"

    @logger.track
    def api_call(endpoint):
        if endpoint == "/error":
            raise ConnectionError("API unreachable")
        return f"Response from {endpoint}"

    # Run functions
    print("Function 1: database_query('users')")
    database_query("users")

    print("\nFunction 2: database_query('invalid')")
    database_query("invalid")

    print("\nFunction 3: api_call('/data')")
    api_call("/data")

    print("\nFunction 4: api_call('/error')")
    api_call("/error")

    # Print report
    logger.report()


# ============================================================================
# PRACTICAL EXAMPLE: Retry Logic
# ============================================================================

def practical_retry_logic():
    """Practical example: Automatic retry logic."""
    print("\n" + "="*70)
    print("PRACTICAL: Automatic Retry Logic")
    print("="*70)

    def retry(max_attempts=3, delay=0.1):
        """Decorator that retries on specific exceptions."""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                last_exception = None
                for attempt in range(max_attempts):
                    try:
                        result = func(*args, **kwargs)
                        if attempt > 0:
                            print(f"✓ Succeeded on attempt {attempt + 1}")
                        return result
                    except (ConnectionError, TimeoutError) as e:
                        last_exception = e
                        if attempt < max_attempts - 1:
                            print(f"✗ Attempt {attempt + 1} failed: {e}, retrying...")
                            time.sleep(delay)
                        else:
                            print(f"✗ All {max_attempts} attempts failed")
                if last_exception:
                    raise last_exception
            return wrapper
        return decorator

    # Use a mutable container to track calls within closure
    call_state = {'count': 0}

    @retry(max_attempts=3, delay=0.1)
    def unstable_api():
        """API that fails first 2 times, succeeds on 3rd."""
        call_state['count'] += 1
        if call_state['count'] < 3:
            raise ConnectionError(f"Connection failed (attempt {call_state['count']})")
        return "Success!"

    # Usage
    call_state['count'] = 0
    result = unstable_api()
    print(f"Result: {result}\n")


# ============================================================================
# Main
# ============================================================================

if __name__ == '__main__':
    print("="*70)
    print("EXCEPTION INTERCEPTION TECHNIQUES - RUNNABLE EXAMPLES")
    print("="*70)

    # Run all examples
    technique_1_try_except()
    technique_2_wrapper()
    technique_3_decorator()
    technique_4_context_manager()
    technique_5_monkey_patching()
    technique_6_class_monkey_patching()
    advanced_combined_approach()
    practical_error_logging()
    practical_retry_logic()

    print("\n" + "="*70)
    print("✅ All examples completed!")
    print("="*70)
