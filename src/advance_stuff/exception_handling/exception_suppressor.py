"""
Python Exception Suppressor - Modern Exception Handling & Suppression

Demonstrates modern Python exception suppression techniques including:
- ExceptionGroup (Python 3.11+)
- except* syntax for group handling
- Structured exception suppression
- Contextual exception handling
- Logging and tracking
"""

import sys
import functools
import traceback
import time
from typing import Type, Callable, Any, Dict, List
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime


# ============================================================================
# MODERN PYTHON 3.11+ FEATURES: ExceptionGroup and except*
# ============================================================================

def demo_exception_group():
    """Demonstrate Python 3.11+ ExceptionGroup and except* syntax."""
    print("\n" + "="*70)
    print("DEMO 1: ExceptionGroup & except* Syntax (Python 3.11+)")
    print("="*70)

    # Python 3.11+ allows except* for exception groups
    if sys.version_info >= (3, 11):
        try:
            # Create multiple exceptions that occur together
            excs = [
                ValueError("Invalid input"),
                TypeError("Wrong type"),
                RuntimeError("Runtime error"),
            ]
            raise ExceptionGroup("Multiple errors", excs)

        except* ValueError as eg:
            print(f"✓ Caught ValueError group: {eg.exceptions}")
        except* TypeError as eg:
            print(f"✓ Caught TypeError group: {eg.exceptions}")
        except* RuntimeError as eg:
            print(f"✓ Caught RuntimeError group: {eg.exceptions}")

        print("Code continues after exception group handling")
    else:
        print("ExceptionGroup requires Python 3.11+")
        print(f"Current version: {sys.version_info.major}.{sys.version_info.minor}")


# ============================================================================
# EXCEPTION SUPPRESSOR CLASS
# ============================================================================

@dataclass
class SuppressedExceptionInfo:
    """Information about a suppressed exception."""
    exception_type: Type[Exception]
    message: str
    traceback: str
    timestamp: datetime
    context: Dict[str, Any]


class ExceptionSuppressor:
    """
    Context manager for suppressing and tracking exceptions.
    Modern approach with logging and categorization.
    """

    def __init__(
        self,
        suppress_types: tuple = Exception,
        log_exceptions: bool = True,
        on_suppress: Callable = None,
        name: str = "Operation"
    ):
        """
        Initialize the suppressor.

        Args:
            suppress_types: Exception type(s) to suppress
            log_exceptions: Whether to log suppressed exceptions
            on_suppress: Callback function when exception is suppressed
            name: Name of the operation being tracked
        """
        self.suppress_types = suppress_types
        self.log_exceptions = log_exceptions
        self.on_suppress = on_suppress
        self.name = name
        self.suppressed: List[SuppressedExceptionInfo] = []

    def __enter__(self):
        """Enter context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager with exception handling."""
        if exc_type is None:
            return False

        # Check if exception should be suppressed
        if isinstance(exc_val, self.suppress_types):
            if self.log_exceptions:
                self._log_exception(exc_type, exc_val, exc_tb)

            if self.on_suppress:
                self.on_suppress(exc_type, exc_val)

            # Return True to suppress the exception
            return True

        # Don't suppress other exceptions
        return False

    def _log_exception(self, exc_type, exc_val, exc_tb):
        """Log a suppressed exception."""
        tb_str = ''.join(traceback.format_tb(exc_tb))
        info = SuppressedExceptionInfo(
            exception_type=exc_type,
            message=str(exc_val),
            traceback=tb_str,
            timestamp=datetime.now(),
            context={'operation': self.name}
        )
        self.suppressed.append(info)

        print(f"⚠️  Suppressed: {exc_type.__name__}: {exc_val}")

    def report(self):
        """Print report of suppressed exceptions."""
        print(f"\n📊 Exception Suppression Report ({self.name})")
        print(f"   Total suppressed: {len(self.suppressed)}")

        if not self.suppressed:
            print("   No exceptions suppressed")
            return

        for i, exc in enumerate(self.suppressed, 1):
            print(f"\n{i}. {exc.exception_type.__name__}")
            print(f"   Message: {exc.message}")
            print(f"   Time: {exc.timestamp.strftime('%H:%M:%S')}")

    def get_summary(self) -> Dict[str, Any]:
        """Get summary of suppression."""
        return {
            'total_suppressed': len(self.suppressed),
            'exception_types': [exc.exception_type.__name__ for exc in self.suppressed],
            'timestamps': [exc.timestamp for exc in self.suppressed],
        }


# ============================================================================
# MODERN DECORATOR-BASED SUPPRESSION
# ============================================================================

def suppress_exceptions(*exception_types, log=True, on_error=None):
    """
    Modern decorator for suppressing exceptions.

    Usage:
        @suppress_exceptions(ValueError, TypeError)
        def my_function():
            raise ValueError("Oops")
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exception_types as e:
                if log:
                    print(f"⚠️  {func.__name__} suppressed: {type(e).__name__}: {e}")
                if on_error:
                    on_error(e)
                return None
        return wrapper
    return decorator


# ============================================================================
# CONTEXTLIB APPROACH: suppress() built-in alternative
# ============================================================================

def demo_contextlib_suppress():
    """Demonstrate built-in contextlib.suppress()."""
    print("\n" + "="*70)
    print("DEMO 2: Built-in contextlib.suppress()")
    print("="*70)

    from contextlib import suppress

    print("\nUsage 1: Suppress single exception type")
    with suppress(ValueError):
        raise ValueError("This is suppressed")
    print("Code continues after suppression")

    print("\nUsage 2: Suppress multiple exception types")
    with suppress(ValueError, TypeError, KeyError):
        data = {}
        data['missing_key']  # Raises KeyError
    print("KeyError was suppressed and code continues")

    print("\nUsage 3: No exception raised (normal flow)")
    with suppress(ValueError):
        print("Normal operation")
        result = int("42")
        print(f"Result: {result}")


# ============================================================================
# ADVANCED: ExceptionHandler with grouping
# ============================================================================

class ExceptionHandler:
    """Advanced exception handler with grouping and filtering."""

    def __init__(self):
        self.exceptions: Dict[Type[Exception], List[Exception]] = {}
        self.total_handled = 0

    @contextmanager
    def handle_and_group(self, *exception_types, suppress=False):
        """Handle exceptions and group them by type."""
        try:
            yield self
        except exception_types as e:
            exc_type = type(e)

            # Group by exception type
            if exc_type not in self.exceptions:
                self.exceptions[exc_type] = []
            self.exceptions[exc_type].append(e)
            self.total_handled += 1

            print(f"⚠️  Handled: {exc_type.__name__}: {e}")

            if not suppress:
                raise

    def report_by_type(self):
        """Report exceptions grouped by type."""
        print(f"\n📊 Exception Report (Total: {self.total_handled})")

        if not self.exceptions:
            print("   No exceptions handled")
            return

        for exc_type, excs in self.exceptions.items():
            print(f"\n   {exc_type.__name__}: {len(excs)} occurrences")
            for i, exc in enumerate(excs[:3], 1):  # Show first 3
                print(f"      {i}. {exc}")
            if len(excs) > 3:
                print(f"      ... and {len(excs) - 3} more")

    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about handled exceptions."""
        return {
            'total_handled': self.total_handled,
            'exception_types': len(self.exceptions),
            'by_type': {
                exc_type.__name__: len(excs)
                for exc_type, excs in self.exceptions.items()
            }
        }


# ============================================================================
# RETRY WITH EXCEPTION SUPPRESSION
# ============================================================================

def suppress_with_retry(max_retries=3, delay=0.5, on_final_failure=None):
    """
    Decorator combining retry logic with exception suppression.
    Suppresses exception after max retries.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_retries):
                try:
                    result = func(*args, **kwargs)
                    if attempt > 0:
                        print(f"✓ Succeeded on attempt {attempt + 1}")
                    return result

                except Exception as e:
                    last_exception = e
                    print(f"✗ Attempt {attempt + 1} failed: {e}")

                    if attempt < max_retries - 1:
                        time.sleep(delay)
                    else:
                        # Final attempt failed - suppress and call callback
                        print(f"⚠️  Suppressing exception after {max_retries} attempts")
                        if on_final_failure:
                            on_final_failure(e)
                        return None

        return wrapper
    return decorator


# ============================================================================
# DEMO USAGE
# ============================================================================

def demo_exception_suppressor_context():
    """Demonstrate ExceptionSuppressor context manager."""
    print("\n" + "="*70)
    print("DEMO 3: ExceptionSuppressor Context Manager")
    print("="*70)

    def on_suppress_callback(exc_type, exc_val):
        print(f"   Callback triggered for {exc_type.__name__}")

    print("\nExample 1: Suppress single operation")
    with ExceptionSuppressor(
        suppress_types=(ValueError,),
        name="Validation"
    ) as suppressor:
        raise ValueError("Invalid input")

    suppressor.report()

    print("\n\nExample 2: Suppress multiple exception types")
    with ExceptionSuppressor(
        suppress_types=(ValueError, TypeError),
        on_suppress=on_suppress_callback,
        name="MultiType"
    ) as suppressor:
        raise TypeError("Wrong type")

    suppressor.report()

    print("\n\nExample 3: Multiple operations")
    with ExceptionSuppressor(
        suppress_types=(ValueError, KeyError),
        name="DataProcessing"
    ) as suppressor:
        # First operation succeeds
        data = {"key": "value"}
        print(f"Data: {data}")

        # Second operation fails but is suppressed
        try:
            raise ValueError("Bad value")
        except:
            # Let the context manager handle it
            raise

    suppressor.report()


def demo_suppress_decorator():
    """Demonstrate suppress_exceptions decorator."""
    print("\n" + "="*70)
    print("DEMO 4: suppress_exceptions Decorator")
    print("="*70)

    def error_callback(exc):
        print(f"   Error callback: {exc}")

    @suppress_exceptions(ValueError, TypeError, log=True, on_error=error_callback)
    def risky_conversion(value, target_type):
        """Function that might raise exceptions."""
        if target_type == int:
            return int(value)  # Might raise ValueError
        elif target_type == float:
            return float(value)  # Might raise ValueError
        else:
            return None

    print("\nCalling with valid input:")
    result = risky_conversion("42", int)
    print(f"Result: {result}")

    print("\nCalling with invalid input (exception suppressed):")
    result = risky_conversion("not-a-number", int)
    print(f"Result: {result}")

    print("\nCalling with another exception (also suppressed):")
    @suppress_exceptions(ZeroDivisionError)
    def divide(a, b):
        return a / b

    result = divide(10, 0)
    print(f"Result after division by zero: {result}")


def demo_exception_handler_grouping():
    """Demonstrate ExceptionHandler with grouping."""
    print("\n" + "="*70)
    print("DEMO 5: Exception Grouping & Analysis")
    print("="*70)

    handler = ExceptionHandler()

    print("\nProcessing operations with exception handling:")

    operations = [
        ("Parse JSON", '{"invalid"}'),
        ("Convert int", "not-a-number"),
        ("Parse JSON", '{"another": "invalid"}'),
        ("Convert int", "123"),  # Success
        ("Convert int", "abc"),
        ("Parse JSON", '{"ok": true}'),  # Success
    ]

    for op_name, data in operations:
        try:
            with handler.handle_and_group(ValueError, suppress=True):
                if op_name == "Parse JSON":
                    if data.startswith('{') and not data.endswith('}'):
                        raise ValueError(f"Invalid JSON: {data}")
                    print(f"✓ {op_name}: OK")
                elif op_name == "Convert int":
                    int(data)
                    print(f"✓ {op_name}: OK")
        except ValueError:
            pass

    handler.report_by_type()
    stats = handler.get_stats()
    print(f"\nStats: {stats}")


def demo_retry_with_suppression():
    """Demonstrate retry with eventual suppression."""
    print("\n" + "="*70)
    print("DEMO 6: Retry with Exception Suppression")
    print("="*70)

    attempt_count = 0

    def on_failure(exc):
        print(f"   Final callback: Operation failed with {type(exc).__name__}")

    @suppress_with_retry(max_retries=3, delay=0.1, on_final_failure=on_failure)
    def unstable_operation():
        """Simulates an operation that always fails."""
        nonlocal attempt_count
        attempt_count += 1
        raise ConnectionError(f"Connection attempt {attempt_count} failed")

    print("\nCalling unstable operation (will retry 3 times, then suppress):")
    result = unstable_operation()
    print(f"Final result (suppressed): {result}")


# ============================================================================
# MODERN PATTERN: Silent Failures with Logging
# ============================================================================

class SilentFailureHandler:
    """Handle failures silently with logging for debugging."""

    def __init__(self, operation_name: str):
        self.operation_name = operation_name
        self.failure_log: List[Dict] = []

    @contextmanager
    def silent_context(self):
        """Context that silently handles failures."""
        try:
            yield
        except Exception as e:
            self._log_failure(e)

    def _log_failure(self, exc: Exception):
        """Log failure for debugging."""
        self.failure_log.append({
            'type': type(exc).__name__,
            'message': str(exc),
            'timestamp': datetime.now(),
        })
        # Silently continue - exception is suppressed

    def has_failures(self) -> bool:
        """Check if any failures occurred."""
        return len(self.failure_log) > 0

    def get_failures(self) -> List[Dict]:
        """Get list of failures."""
        return self.failure_log


def demo_silent_failures():
    """Demonstrate silent failure handling."""
    print("\n" + "="*70)
    print("DEMO 7: Silent Failure Handling with Logging")
    print("="*70)

    handler = SilentFailureHandler("DataProcessor")

    print("\nProcessing multiple items (failures are silent):")

    items = [1, "two", 3, None, 5, "invalid"]

    for i, item in enumerate(items, 1):
        with handler.silent_context():
            # Operation that might fail
            result = item * 2
            print(f"  Item {i}: {item} × 2 = {result}")

    print(f"\nProcessing complete. Has failures: {handler.has_failures()}")

    if handler.has_failures():
        print("Failures detected:")
        for i, failure in enumerate(handler.get_failures(), 1):
            print(f"  {i}. {failure['type']}: {failure['message']}")


# ============================================================================
# Main
# ============================================================================

if __name__ == '__main__':
    print("="*70)
    print("PYTHON EXCEPTION SUPPRESSOR - MODERN TECHNIQUES")
    print("="*70)
    print(f"Python {sys.version_info.major}.{sys.version_info.minor}")

    # Run demonstrations
    if sys.version_info >= (3, 11):
        demo_exception_group()

    demo_contextlib_suppress()
    demo_exception_suppressor_context()
    demo_suppress_decorator()
    demo_exception_handler_grouping()
    demo_retry_with_suppression()
    demo_silent_failures()

    print("\n" + "="*70)
    print("✅ All exception suppression demos completed!")
    print("="*70)
