# Python Code Coverage Guide

A comprehensive guide to measuring and improving code coverage in Python applications.

---

## Table of Contents
1. [What is Code Coverage?](#what-is-code-coverage)
2. [Why Code Coverage Matters](#why-code-coverage-matters)
3. [Tools Available](#tools-available)
4. [Quick Start](#quick-start)
5. [Step-by-Step Setup](#step-by-step-setup)
6. [Running Coverage](#running-coverage)
7. [Analyzing Results](#analyzing-results)
8. [Best Practices](#best-practices)
9. [Advanced Usage](#advanced-usage)

---

## What is Code Coverage?

**Code coverage** measures how much of your source code is executed by your tests.

### Coverage Metrics

| Metric | What It Measures |
|--------|------------------|
| **Line Coverage** | % of lines executed |
| **Branch Coverage** | % of conditional branches taken |
| **Function Coverage** | % of functions called |
| **Statement Coverage** | % of statements executed |

### Example

```python
def check_age(age):
    if age >= 18:          # Line 1
        return "Adult"     # Line 2 (only executed if age >= 18)
    else:                  # Line 3
        return "Minor"     # Line 4 (only executed if age < 18)

# Test with age = 25
result = check_age(25)
# Coverage: 75% (Lines 1, 2, 3 executed; Line 4 NOT executed)
```

---

## Why Code Coverage Matters

✓ **Identifies untested code** - Reveals gaps in testing
✓ **Reduces bugs** - Well-tested code = fewer bugs in production
✓ **Improves code quality** - Forces you to write better tests
✓ **Prevents regressions** - Catches breaking changes
✓ **Documents behavior** - Tests show how code is intended to work
✓ **Builds confidence** - Know your code works before deployment

### Industry Standards
- **Good:** 80% coverage
- **Excellent:** 90%+ coverage
- **Unrealistic:** 100% (some code is hard/impossible to test)

---

## Tools Available

### Primary Tools

| Tool | Type | Best For |
|------|------|----------|
| **coverage.py** | Standalone | Detailed analysis, HTML reports |
| **pytest-cov** | Pytest plugin | Running with pytest |
| **unittest coverage** | Built-in | Simple unittest projects |

### We'll Use: `coverage.py` + `pytest-cov`

---

## Quick Start

### 1. Install Tools
```bash
pip install coverage pytest pytest-cov
```

### 2. Run Coverage
```bash
# Using pytest-cov (easiest)
pytest --cov=. tests/

# Using coverage.py directly
coverage run -m pytest tests/
coverage report
coverage html
```

### 3. View Results
```bash
# Terminal report
coverage report

# Open HTML report in browser
open htmlcov/index.html
```

---

## Step-by-Step Setup

### Step 1: Create Project Structure
```
my_project/
├── src/
│   ├── __init__.py
│   ├── calculator.py
│   └── utils.py
├── tests/
│   ├── __init__.py
│   ├── test_calculator.py
│   └── test_utils.py
├── .coveragerc          # Configuration file (optional)
└── pytest.ini           # Pytest configuration (optional)
```

### Step 2: Install Coverage Tools
```bash
cd my_project
pip install coverage pytest pytest-cov
```

### Step 3: Create Sample Code to Test

**`src/calculator.py`:**
```python
def add(a, b):
    """Add two numbers"""
    return a + b

def subtract(a, b):
    """Subtract two numbers"""
    return a - b

def divide(a, b):
    """Divide two numbers"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def multiply(a, b):
    """Multiply two numbers"""
    return a * b
```

### Step 4: Create Tests

**`tests/test_calculator.py`:**
```python
import pytest
from src.calculator import add, subtract, divide, multiply

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0

def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(0, 5) == -5

def test_multiply():
    assert multiply(3, 4) == 12
    assert multiply(0, 5) == 0

def test_divide():
    assert divide(10, 2) == 5
    assert divide(9, 3) == 3

def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)
```

### Step 5: Verify Tests Work
```bash
pytest tests/
```

Expected output:
```
tests/test_calculator.py::test_add PASSED
tests/test_calculator.py::test_subtract PASSED
tests/test_calculator.py::test_multiply PASSED
tests/test_calculator.py::test_divide PASSED
tests/test_calculator.py::test_divide_by_zero PASSED

====== 5 passed in 0.05s ======
```

---

## Running Coverage

### Method 1: Using pytest-cov (Easiest)

**Basic Usage:**
```bash
pytest --cov=src tests/
```

**With HTML Report:**
```bash
pytest --cov=src --cov-report=html tests/
```

**With Terminal Report:**
```bash
pytest --cov=src --cov-report=term-missing tests/
```

### Method 2: Using coverage.py

**Step 1: Run tests with coverage tracking**
```bash
coverage run -m pytest tests/
```

**Step 2: Generate report**
```bash
# Terminal report
coverage report

# HTML report
coverage html

# Missing line report
coverage report --skip-covered
```

**Step 3: View HTML report**
```bash
open htmlcov/index.html
```

### Method 3: Combined Approach (Recommended)

```bash
# Run with coverage, show report, generate HTML
pytest --cov=src --cov-report=term-missing --cov-report=html tests/
```

---

## Analyzing Results

### Terminal Report Example

```
Name                    Stmts   Miss  Cover   Missing
-----------------------------------------------------
src/calculator.py          16      2    87%   25-26
src/utils.py              10      5    50%   8-12
-----------------------------------------------------
TOTAL                      26      7    73%
```

### What This Means

| Column | Meaning |
|--------|---------|
| **Name** | Module name |
| **Stmts** | Total statements in code |
| **Miss** | Statements NOT executed by tests |
| **Cover** | Percentage of code covered |
| **Missing** | Line numbers not executed |

### Missing Lines Example

```python
def divide(a, b):
    if b == 0:           # Line 25 - TESTED
        raise ValueError # Line 26 - NOT TESTED (missing)
    return a / b
```

If line 26 shows as missing, it means you never tested the error case. Add a test for it:

```python
def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)  # This tests line 26
```

---

## Interpreting HTML Report

After running `pytest --cov=src --cov-report=html tests/`, open `htmlcov/index.html`:

### Index Page
- Shows overall coverage percentage
- Lists each file with coverage stats
- Color-coded: green (covered), red (not covered)

### Detailed View
Click any file to see:
- Green lines: Executed by tests
- Red lines: NOT executed by tests
- Orange lines: Partial execution (some branches missed)

### Example
```python
def check_age(age):
    if age >= 18:          # Green (tested with age=25)
        return "Adult"     # Green (executed)
    else:                  # Orange (tested but not in this condition)
        return "Minor"     # Red (NOT tested - no test with age < 18)
```

---

## Best Practices

### 1. Set Coverage Goals
```bash
# Fail if coverage drops below 80%
pytest --cov=src --cov-fail-under=80 tests/
```

### 2. Use Configuration File

**`pytest.ini`:**
```ini
[pytest]
testpaths = tests
addopts = --cov=src --cov-report=html --cov-report=term-missing

[coverage:run]
source = src
omit =
    */tests/*
    */migrations/*
```

**`.coveragerc`:**
```ini
[run]
source = src
omit =
    */tests/*
    */__pycache__/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
```

### 3. Skip Lines from Coverage

Use pragma comments for lines that shouldn't be covered:

```python
def debug_print(msg):
    print(f"DEBUG: {msg}")  # pragma: no cover
```

### 4. Test Edge Cases

```python
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# Test BOTH paths
def test_divide_success():
    assert divide(10, 2) == 5

def test_divide_error():
    with pytest.raises(ValueError):
        divide(10, 0)
```

### 5. Continuous Integration

Add to CI/CD pipeline:
```yaml
# GitHub Actions example
- name: Run tests with coverage
  run: |
    pytest --cov=src --cov-fail-under=80 tests/
    coverage html

- name: Upload coverage
  uses: codecov/codecov-action@v3
```

---

## Advanced Usage

### Exclude Specific Directories

```bash
# Exclude tests, migrations, venv
pytest --cov=src --cov-report=html \
  --cov-report=term-missing \
  --no-cov-on-fail \
  tests/
```

### Branch Coverage

```bash
pytest --cov=src --cov-branch --cov-report=html tests/
```

Shows which conditional branches are tested:
```python
if condition:      # Branch 1
    do_something()
else:              # Branch 2
    do_other()
```

### Parallel Testing with Coverage

```bash
# Install pytest-xdist
pip install pytest-xdist

# Run in parallel
pytest --cov=src --cov-report=term-missing -n auto tests/
```

### Generate Coverage Report in Different Formats

```bash
# XML (for tools like SonarQube)
coverage xml

# JSON
coverage json

# LCOV
coverage lcov
```

### Combining Coverage from Multiple Runs

```bash
# Run tests on different Python versions
coverage run -m pytest tests/
coverage run -a -m pytest tests/  # Append to existing data

# Combine results
coverage combine

# Report
coverage report
```

---

## Real-World Workflow

### Day 1: Initial Setup
```bash
# 1. Install tools
pip install coverage pytest pytest-cov

# 2. Run tests
pytest tests/

# 3. Check coverage
pytest --cov=src --cov-report=term-missing tests/

# 4. View detailed report
pytest --cov=src --cov-report=html tests/
open htmlcov/index.html
```

### Day 2-N: Improve Coverage
```bash
# 1. Identify untested code (red lines in HTML report)
# 2. Write tests for missing code
# 3. Verify new tests pass
pytest tests/

# 4. Check coverage improved
pytest --cov=src --cov-report=term-missing tests/

# 5. Ensure you meet minimum threshold
pytest --cov=src --cov-fail-under=80 tests/
```

---

## Common Issues & Solutions

### Issue 1: "No coverage data"
```bash
# Solution: Make sure you're in the right directory
pwd
# Should output your project directory

# Run with full paths
pytest --cov=src --cov-report=html ./tests/
```

### Issue 2: "coverage command not found"
```bash
# Solution: Install coverage
pip install coverage

# Or use python module
python -m coverage report
```

### Issue 3: "Import errors"
```bash
# Solution: Make sure __init__.py exists
touch src/__init__.py
touch tests/__init__.py

# Add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Issue 4: "Coverage percentage is very low"
```bash
# Solution: You're missing tests. Write more tests for uncovered code
# Check the HTML report: htmlcov/index.html
# Red lines = untested code
```

### Issue 5: "Some lines marked as missing but are tested"
```python
# Solution: Mark excluded lines with pragma
def debug_only():
    print("debug")  # pragma: no cover

# Or configure .coveragerc to exclude
[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise NotImplementedError
```

---

## Example: Full Coverage Workflow

### 1. Project Structure
```
my_project/
├── src/
│   ├── __init__.py
│   ├── math_ops.py
│   └── string_ops.py
├── tests/
│   ├── __init__.py
│   └── test_*.py
├── .coveragerc
├── pytest.ini
└── requirements.txt
```

### 2. Configuration Files

**`pytest.ini`:**
```ini
[pytest]
testpaths = tests
addopts = --verbose --strict-markers
```

**`.coveragerc`:**
```ini
[run]
source = src
branch = True

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise NotImplementedError
    if __name__ == .__main__.:

exclude_dirs =
    */tests
    */migrations
```

### 3. Run Everything

```bash
# Run tests with coverage, show detailed report
pytest --cov=src --cov-report=term-missing --cov-report=html

# Check threshold
pytest --cov=src --cov-fail-under=80

# View HTML
open htmlcov/index.html
```

---

## Summary Checklist

- [ ] Install `coverage` and `pytest-cov`
- [ ] Write tests for your code
- [ ] Run `pytest --cov=src tests/`
- [ ] Review terminal report
- [ ] Generate HTML report: `pytest --cov=src --cov-report=html`
- [ ] Open `htmlcov/index.html` in browser
- [ ] Identify red (uncovered) lines
- [ ] Write additional tests for missing code
- [ ] Rerun coverage until satisfied
- [ ] Set minimum threshold (e.g., 80%)
- [ ] Add to CI/CD pipeline

---

## Resources

- [coverage.py Documentation](https://coverage.readthedocs.io/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [Python Testing Best Practices](https://docs.python-guide.org/writing/tests/)
- [Code Coverage Tutorial](https://www.atlassian.com/continuous-delivery/software-testing/code-coverage)

---

## Next Steps

1. **Start Simple:** Test one module completely
2. **Iteratively Improve:** Add tests for other modules
3. **Set Goals:** Aim for 80%+ coverage
4. **Automate:** Add to CI/CD pipeline
5. **Monitor:** Track coverage over time

Happy testing! 🧪
