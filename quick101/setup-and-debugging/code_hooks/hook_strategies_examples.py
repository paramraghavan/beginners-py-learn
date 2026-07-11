"""
Hook Strategies Examples: Practical implementations of various interception techniques.

Demonstrates:
1. Function/Method wrapping hooks
2. Attribute access hooks
3. Module import hooks
4. Metaclass hooks
5. Descriptor hooks
6. Context manager hooks
7. Proxy pattern hooks
"""

import functools
import sys
from typing import Any, Dict
from contextlib import contextmanager


# ============================================================================
# HOOK 1: Function Wrapping (Decorator)
# ============================================================================

def hook_1_function_wrapping():
    """Hook into function calls using decorators."""
    print("\n" + "="*70)
    print("HOOK 1: Function Wrapping (Decorator)")
    print("="*70)

    def log_calls(func):
        """Decorator that logs function calls."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"→ Calling: {func.__name__}{args}{kwargs}")
            try:
                result = func(*args, **kwargs)
                print(f"← Returned: {result}")
                return result
            except Exception as e:
                print(f"✗ Exception: {type(e).__name__}: {e}")
                raise
        return wrapper

    @log_calls
    def divide(a, b):
        return a / b

    @log_calls
    def greet(name):
        return f"Hello, {name}!"

    # Usage
    print("\nSuccessful call:")
    divide(10, 2)

    print("\nFailed call:")
    try:
        divide(10, 0)
    except ZeroDivisionError:
        pass

    print("\nMultiple calls:")
    greet("Alice")
    greet("Bob")


# ============================================================================
# HOOK 2: Attribute Access (Property)
# ============================================================================

def hook_2_property_access():
    """Hook into attribute access using properties."""
    print("\n" + "="*70)
    print("HOOK 2: Attribute Access (Property)")
    print("="*70)

    class BankAccount:
        def __init__(self, balance):
            self._balance = balance
            self._access_count = 0

        @property
        def balance(self):
            """Property that tracks reads."""
            self._access_count += 1
            print(f"  📖 Reading balance (access #{self._access_count})")
            return self._balance

        @balance.setter
        def balance(self, value):
            """Property that validates writes."""
            print(f"  💾 Setting balance: ${self._balance} → ${value}")
            if value < 0:
                print(f"  ✗ Rejected: balance cannot be negative")
                raise ValueError("Balance cannot be negative")
            self._balance = value

    # Usage
    account = BankAccount(1000)
    print("\nReading balance:")
    print(f"Balance: ${account.balance}")

    print("\nReading again:")
    print(f"Balance: ${account.balance}")

    print("\nSetting valid balance:")
    account.balance = 1500

    print("\nSetting invalid balance:")
    try:
        account.balance = -100
    except ValueError:
        pass


# ============================================================================
# HOOK 3: Attribute Access (__getattr__)
# ============================================================================

def hook_3_getattr():
    """Hook into missing attribute access."""
    print("\n" + "="*70)
    print("HOOK 3: Attribute Access (__getattr__)")
    print("="*70)

    class DynamicObject:
        """Object that generates attributes dynamically."""
        def __init__(self, name):
            self.name = name
            self._access_log = []

        def __getattr__(self, attr):
            """Called when attribute is not found."""
            self._access_log.append(attr)
            print(f"  🔍 Dynamically creating: {attr}")
            # Generate attribute on the fly
            return f"<dynamic value for {attr}>"

        def show_access_log(self):
            """Show what was accessed."""
            print(f"  Access log: {self._access_log}")

    # Usage
    obj = DynamicObject("TestObject")

    print("\nAccessing existing attribute:")
    print(f"Name: {obj.name}")

    print("\nAccessing missing attributes (generated dynamically):")
    print(f"obj.greeting = {obj.greeting}")
    print(f"obj.config = {obj.config}")
    print(f"obj.data = {obj.data}")

    print("\nAccess pattern:")
    obj.show_access_log()


# ============================================================================
# HOOK 4: Comprehensive Attribute Access (__getattribute__)
# ============================================================================

def hook_4_getattribute():
    """Hook into ALL attribute access."""
    print("\n" + "="*70)
    print("HOOK 4: Comprehensive Attribute Access (__getattribute__)")
    print("="*70)

    class FullyTracked:
        """Tracks ALL attribute access."""
        def __init__(self, value):
            object.__setattr__(self, '_value', value)
            object.__setattr__(self, '_access_count', 0)

        def __getattribute__(self, name):
            # Be careful: called for EVERYTHING including special methods
            if not name.startswith('_') and name not in ['show_stats']:
                count = object.__getattribute__(self, '_access_count')
                object.__setattr__(self, '_access_count', count + 1)
                print(f"  ↻ Accessed: {name} (access #{count + 1})")

            return object.__getattribute__(self, name)

        def show_stats(self):
            count = object.__getattribute__(self, '_access_count')
            print(f"  📊 Total non-private accesses: {count}")

    # Usage
    obj = FullyTracked(42)

    print("\nAccessing attributes:")
    val = obj._value
    obj.show_stats()

    # Note: This hook is SLOW because it's called for everything!
    # Use __getattr__ (fallback only) unless you need to track everything


# ============================================================================
# HOOK 5: Proxy Pattern
# ============================================================================

def hook_5_proxy_pattern():
    """Hook into all interactions via proxy."""
    print("\n" + "="*70)
    print("HOOK 5: Proxy Pattern")
    print("="*70)

    class Calculator:
        def add(self, a, b):
            return a + b
        def multiply(self, a, b):
            return a * b

    class TrackedProxy:
        """Proxy that tracks all interactions."""
        def __init__(self, obj):
            object.__setattr__(self, '_obj', obj)
            object.__setattr__(self, '_calls', [])

        def __getattr__(self, name):
            obj = object.__getattribute__(self, '_obj')
            attr = getattr(obj, name)

            # Track method calls
            if callable(attr):
                def tracked_call(*args, **kwargs):
                    print(f"  ⚙️  Calling: {name}{args}")
                    result = attr(*args, **kwargs)
                    print(f"  ← Result: {result}")

                    # Log the call
                    calls = object.__getattribute__(self, '_calls')
                    calls.append({'method': name, 'args': args, 'result': result})
                    return result

                return tracked_call
            else:
                print(f"  📍 Accessing: {name}")
                return attr

        def get_call_history(self):
            calls = object.__getattribute__(self, '_calls')
            return calls

    # Usage
    calc = Calculator()
    tracked_calc = TrackedProxy(calc)

    print("\nCalling methods through proxy:")
    tracked_calc.add(2, 3)
    tracked_calc.multiply(4, 5)

    print("\nCall history:")
    for call in tracked_calc.get_call_history():
        print(f"  {call['method']} → {call['result']}")


# ============================================================================
# HOOK 6: Metaclass Hooks
# ============================================================================

def hook_6_metaclass():
    """Hook into class creation and modification."""
    print("\n" + "="*70)
    print("HOOK 6: Metaclass Hooks")
    print("="*70)

    class InstrumentedMeta(type):
        """Metaclass that instruments all methods."""
        def __new__(mcs, name, bases, dct):
            print(f"  📋 Creating class: {name}")

            # Wrap all methods
            for key, value in dct.items():
                if callable(value) and not key.startswith('_'):
                    dct[key] = mcs.wrap_method(value, key)

            return super().__new__(mcs, name, bases, dct)

        @staticmethod
        def wrap_method(method, method_name):
            """Wrap a method with logging."""
            @functools.wraps(method)
            def wrapper(self, *args, **kwargs):
                print(f"  → {method_name}{args}")
                result = method(self, *args, **kwargs)
                print(f"  ← {result}")
                return result
            return wrapper

    class MyService(metaclass=InstrumentedMeta):
        """Service with auto-instrumented methods."""
        def fetch_data(self, source):
            return f"Data from {source}"

        def process(self, data):
            return f"Processed: {data}"

    # Usage
    print("\nUsing auto-instrumented class:")
    service = MyService()
    service.fetch_data("API")
    service.process("raw data")


# ============================================================================
# HOOK 7: Descriptor Hooks
# ============================================================================

def hook_7_descriptor():
    """Hook into attribute access using descriptors."""
    print("\n" + "="*70)
    print("HOOK 7: Descriptor Hooks")
    print("="*70)

    class ValidatedDescriptor:
        """Descriptor that validates on set."""
        def __init__(self, name, expected_type):
            self.name = name
            self.expected_type = expected_type
            self.data = {}

        def __get__(self, obj, objtype=None):
            if obj is None:
                return self
            obj_id = id(obj)
            if obj_id in self.data:
                print(f"  📖 Reading {self.name}: {self.data[obj_id]}")
                return self.data[obj_id]
            return None

        def __set__(self, obj, value):
            if not isinstance(value, self.expected_type):
                print(f"  ✗ Type error: {self.name} expects {self.expected_type.__name__}")
                raise TypeError(f"Expected {self.expected_type}, got {type(value)}")
            print(f"  💾 Setting {self.name}: {value}")
            self.data[id(obj)] = value

    class Person:
        name = ValidatedDescriptor('name', str)
        age = ValidatedDescriptor('age', int)

    # Usage
    print("\nUsing descriptor validation:")
    person = Person()

    print("\nSetting valid values:")
    person.name = "Alice"
    person.age = 30

    print("\nAccessing values:")
    print(f"Name: {person.name}")
    print(f"Age: {person.age}")

    print("\nSetting invalid value:")
    try:
        person.age = "thirty"
    except TypeError:
        pass


# ============================================================================
# HOOK 8: Import Hooks (sys.modules patching)
# ============================================================================

def hook_8_import_hooks():
    """Hook into module imports."""
    print("\n" + "="*70)
    print("HOOK 8: Import Hooks (sys.modules Patching)")
    print("="*70)

    # Create a fake module
    import types
    fake_module = types.ModuleType('fake_lib')
    fake_module.value = 42

    def fake_function():
        return "Fake response"

    fake_module.fake_function = fake_function

    # Save the original (if it exists)
    original = sys.modules.get('fake_lib', None)

    try:
        # Patch sys.modules
        sys.modules['fake_lib'] = fake_module
        print("\n  ✓ Patched sys.modules['fake_lib']")

        # Now import uses our patched version
        import fake_lib
        print(f"  ✓ Imported fake_lib")
        print(f"  Value: {fake_lib.value}")
        print(f"  Function: {fake_lib.fake_function()}")

    finally:
        # Restore
        if original:
            sys.modules['fake_lib'] = original
        elif 'fake_lib' in sys.modules:
            del sys.modules['fake_lib']
        print("\n  ✓ Restored sys.modules")


# ============================================================================
# HOOK 9: Context Manager Hooks
# ============================================================================

def hook_9_context_manager():
    """Hook into resource lifecycle."""
    print("\n" + "="*70)
    print("HOOK 9: Context Manager Hooks")
    print("="*70)

    class ResourceManager:
        """Context manager that tracks resource lifecycle."""
        def __init__(self, resource_name):
            self.resource_name = resource_name
            self.operations = []

        def __enter__(self):
            print(f"  🔓 Acquiring: {self.resource_name}")
            self.operations.append('acquire')
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            print(f"  🔒 Releasing: {self.resource_name}")
            self.operations.append('release')

            if exc_type is not None:
                print(f"  ⚠️  Exception: {exc_type.__name__}: {exc_val}")
                self.operations.append(f'exception: {exc_type.__name__}')

            # Return False to propagate exception
            return False

        def do_work(self, work_desc):
            print(f"  ⚙️  {work_desc}")
            self.operations.append(work_desc)

        def show_log(self):
            print(f"  📋 Operation log:")
            for op in self.operations:
                print(f"     - {op}")

    # Usage
    print("\nNormal usage:")
    with ResourceManager("database connection") as rm:
        rm.do_work("Execute query 1")
        rm.do_work("Execute query 2")
    rm.show_log()

    print("\nUsage with exception:")
    try:
        with ResourceManager("file handle") as rm:
            rm.do_work("Read data")
            raise ValueError("Simulated error")
            rm.do_work("This won't run")
    except ValueError:
        pass
    rm.show_log()


# ============================================================================
# HOOK 10: Combination Pattern (Like permission_analyzer_runtime)
# ============================================================================

def hook_10_combination():
    """Combine multiple hooks for comprehensive interception."""
    print("\n" + "="*70)
    print("HOOK 10: Combination Pattern (Layered Hooks)")
    print("="*70)

    class APISimulator:
        """Simulates an API."""
        def __init__(self):
            self.call_count = 0

        def request(self, endpoint, action):
            self.call_count += 1
            if action == "admin" and self.call_count < 3:
                raise PermissionError(f"Admin action denied")
            return f"Response from {endpoint}"

    class APITracker:
        """Combines: monkey patching + context manager + exception handling."""
        def __init__(self):
            self._original_request = None
            self.tracked_errors = []
            self.call_log = []

        def __enter__(self):
            """Setup: Monkey patch the API."""
            self._original_request = APISimulator.request

            def tracked_request(api_self, endpoint, action):
                self.call_log.append((endpoint, action))
                try:
                    return self._original_request(api_self, endpoint, action)
                except PermissionError as e:
                    self.tracked_errors.append({
                        'endpoint': endpoint,
                        'action': action,
                        'error': str(e)
                    })
                    print(f"  ⚠️  Permission error intercepted: {e}")
                    # Return mock response instead of raising
                    return "Mock response (permission denied)"

            APISimulator.request = tracked_request
            print("  ✓ Patched APISimulator.request")
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            """Cleanup: Restore original."""
            APISimulator.request = self._original_request
            print("  ✓ Restored APISimulator.request")
            return False

        def report(self):
            """Report findings."""
            print(f"\n  📊 API Tracker Report:")
            print(f"     Total calls: {len(self.call_log)}")
            print(f"     Permission errors: {len(self.tracked_errors)}")
            if self.tracked_errors:
                print(f"     Errors:")
                for err in self.tracked_errors:
                    print(f"       - {err['action']} on {err['endpoint']}: {err['error']}")

    # Usage
    api = APISimulator()

    print("\nNormal usage (without tracking):")
    response = api.request("/data", "read")
    print(f"  Response: {response}")

    print("\nWith APITracker:")
    with APITracker() as tracker:
        api.request("/data", "read")
        api.request("/admin", "admin")  # Will error but handled
        api.request("/config", "admin")  # Will error but handled
        api.request("/admin", "admin")  # Will succeed now

    tracker.report()


# ============================================================================
# Main
# ============================================================================

if __name__ == '__main__':
    print("="*70)
    print("HOOK STRATEGIES - PRACTICAL EXAMPLES")
    print("="*70)

    hook_1_function_wrapping()
    hook_2_property_access()
    hook_3_getattr()
    hook_4_getattribute()
    hook_5_proxy_pattern()
    hook_6_metaclass()
    hook_7_descriptor()
    hook_8_import_hooks()
    hook_9_context_manager()
    hook_10_combination()

    print("\n" + "="*70)
    print("✅ All hook strategy examples completed!")
    print("="*70)
