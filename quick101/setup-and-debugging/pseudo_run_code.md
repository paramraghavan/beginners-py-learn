# pseudo /mock run code

Pseudo run a python function called job_runner.py and it has a main, is there a way to mock run an existing python
code and not actually executing the code, like the ast tree and we start to walk from the main method

Yes, there are several ways to mock run Python code without actually executing it! Here are the main approaches:

## 1. AST-based Static Analysis (Your Suggested Approach)

- AST gives you complete control over the analysis
- You can trace exactly what would happen without side effects
- You can parse the code into an AST and walk through it symbolically:

```python
import ast
import inspect


class MockExecutor(ast.NodeVisitor):
    def __init__(self):
        self.call_stack = []
        self.variables = {}
        self.function_calls = []

    def visit_FunctionDef(self, node):
        print(f"Would define function: {node.name}")
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            print(f"Would call function: {func_name}")
            self.function_calls.append(func_name)
        elif isinstance(node.func, ast.Attribute):
            attr_name = node.func.attr
            print(f"Would call method: {attr_name}")
        self.generic_visit(node)

    def visit_Assign(self, node):
        if isinstance(node.targets[0], ast.Name):
            var_name = node.targets[0].id
            print(f"Would assign to variable: {var_name}")
        self.generic_visit(node)


# Usage
with open('job_runner.py', 'r') as f:
    code = f.read()

tree = ast.parse(code)
executor = MockExecutor()

# Find and start from main
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name == 'main':
        print("Starting mock execution from main()")
        executor.visit(node)
```

## 2. Using `unittest.mock` for Runtime Mocking
- unittest.mock handles external dependencies cleanly
- You can build a comprehensive call graph and execution flow

```python
from unittest.mock import patch, MagicMock
import importlib.util

# Mock all external dependencies
with patch('subprocess.run') as mock_subprocess,
        patch('requests.get') as mock_requests,
        patch('os.system') as mock_os_system,
        patch('builtins.open', create=True) as mock_open:
    # Configure mocks
    mock_subprocess.return_value = MagicMock(returncode=0, stdout="mocked output")
    mock_requests.return_value = MagicMock(status_code=200, json=lambda: {"key": "value"})

    # Import and run
    spec = importlib.util.spec_from_file_location("job_runner", "job_runner.py")
    job_runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(job_runner)

    # Now call main
    job_runner.main()
```

## 3. Dry-Run with Monkey Patching

```python
import sys
import types


class DryRunModule:
    def __init__(self, original_module):
        self.original = original_module
        self.calls_made = []

    def __getattr__(self, name):
        attr = getattr(self.original, name)
        if callable(attr):
            def mock_func(*args, **kwargs):
                self.calls_made.append((name, args, kwargs))
                print(f"DRY RUN: Would call {name} with {args}, {kwargs}")
                return None  # or some default return value

            return mock_func
        return attr


# Replace system modules with dry-run versions
original_os = sys.modules.get('os')
original_subprocess = sys.modules.get('subprocess')

# Create dry-run versions
if original_os:
    sys.modules['os'] = DryRunModule(original_os)
if original_subprocess:
    sys.modules['subprocess'] = DryRunModule(original_subprocess)

# Now import your module
import job_runner

job_runner.main()
```

## 4. Custom Execution Context

```python
class MockContext:
    def __init__(self):
        self.operations = []
        self.variables = {}

    def execute_line(self, line_info):
        # Log what would happen instead of doing it
        print(f"Would execute: {line_info}")
        self.operations.append(line_info)


def trace_execution(frame, event, arg):
    if event == 'line':
        filename = frame.f_code.co_filename
        if 'job_runner.py' in filename:
            line_no = frame.f_lineno
            code = frame.f_code
            print(f"Line {line_no}: {code.co_names}")
    return trace_execution


# Set up tracing
import sys

sys.settrace(trace_execution)

# Import and run with tracing
import job_runner

job_runner.main()
```

## 5. Using `dis` Module for Bytecode Analysis

```python
import dis
import types


def analyze_function(func):
    print(f"Analyzing function: {func.__name__}")
    instructions = list(dis.get_instructions(func))

    for instr in instructions:
        if instr.opname == 'CALL_FUNCTION':
            print(f"Would make function call")
        elif instr.opname == 'STORE_NAME':
            print(f"Would store to variable: {instr.argval}")
        elif instr.opname == 'LOAD_GLOBAL':
            print(f"Would load global: {instr.argval}")


# Load your module
import job_runner

if hasattr(job_runner, 'main'):
    analyze_function(job_runner.main)
```

>Best start with approach #1 (AST walking) combined with #2 (unittest.mock) because:

