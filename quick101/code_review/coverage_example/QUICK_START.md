# Code Coverage - Quick Start Example

This is a working example to learn code coverage in Python.

---

## 📁 What's Included

```
coverage_example/
├── src/
│   ├── __init__.py
│   └── calculator.py        # Module to test
├── tests/
│   ├── __init__.py
│   └── test_calculator.py   # Tests for calculator
├── .coveragerc              # Coverage configuration
├── pytest.ini               # Pytest configuration
├── requirements.txt         # Dependencies
└── QUICK_START.md           # This file
```

---

## 🚀 Step 1: Install Dependencies

```bash
cd coverage_example

# Option A: Using pip directly
pip install pytest pytest-cov coverage

# Option B: Using requirements file
pip install -r requirements.txt
```

---

## 🧪 Step 2: Run Tests Without Coverage

```bash
pytest tests/
```

**Expected Output:**
```
tests/test_calculator.py::TestAddition::test_add_positive_numbers PASSED
tests/test_calculator.py::TestAddition::test_add_negative_numbers PASSED
tests/test_calculator.py::TestAddition::test_add_zero PASSED
... (more tests)

====== 19 passed in 0.XX s ======
```

---

## 📊 Step 3: Run Tests WITH Coverage

### Option A: Simple Report (Terminal)

```bash
pytest --cov=src tests/
```

**Output:**
```
Name            Stmts   Miss  Cover
-----------------------------------
src/__init__.py     1      0   100%
src/calculator.py  31      5    84%
-----------------------------------
TOTAL              32      5    84%
```

### Option B: Detailed Report (Show Missing Lines)

```bash
pytest --cov=src --cov-report=term-missing tests/
```

**Output:**
```
Name                 Stmts   Miss  Cover   Missing
--------------------------------------------------
src/__init__.py          1      0   100%
src/calculator.py       31      5    84%   36, 41, 46, 51, 56
--------------------------------------------------
TOTAL                   32      5    84%
```

**What This Means:**
- 84% of code is covered by tests
- Lines 36, 41, 46, 51, 56 are NOT tested
- These are the error handling branches (`raise ValueError`)

### Option C: HTML Report (Visual)

```bash
pytest --cov=src --cov-report=html tests/
```

**Then open the report:**
```bash
# macOS
open htmlcov/index.html

# Linux
firefox htmlcov/index.html

# Windows
start htmlcov/index.html
```

---

## 📈 Step 4: Analyze the Report

### From Terminal Report

Look for the **Missing** column:
```
Missing: 36, 41, 46, 51, 56
```

These line numbers correspond to untested code. View them:

```bash
cat -n src/calculator.py | grep -E "36|41|46|51|56"
```

### From HTML Report

1. Open `htmlcov/index.html` in browser
2. Click `src/calculator.py`
3. See color-coded lines:
   - **Green** = Tested
   - **Red** = Not tested
   - **Orange** = Partially tested

---

## ✍️ Step 5: Improve Coverage

### Current Gaps

The tests don't cover error cases:
- `divide` with 0
- `power` with negative exponent

### Add Missing Tests

Edit `tests/test_calculator.py` and add more tests for edge cases:

```python
def test_divide_by_zero_edge_case():
    """Additional edge case for divide"""
    with pytest.raises(ValueError):
        divide(100, 0)

def test_power_large_exponent():
    """Test power with large exponent"""
    assert power(2, 10) == 1024

def test_absolute_large_negative():
    """Test absolute with large negative"""
    assert absolute(-999999) == 999999
```

### Rerun Coverage

```bash
pytest --cov=src --cov-report=term-missing tests/
```

You should see coverage percentage increase! 📈

---

## 🎯 Step 6: Set Coverage Threshold

Make tests fail if coverage drops below 80%:

```bash
pytest --cov=src --cov-fail-under=80 tests/
```

**Success (>80%):**
```
TOTAL: 84% (passes)
```

**Failure (<80%):**
```
TOTAL: 75% (fails)
===== FAILED - Coverage below 80% =====
```

---

## 🔧 Complete One-Liners

### Just Run Tests
```bash
pytest tests/
```

### Simple Coverage Report
```bash
pytest --cov=src tests/
```

### Detailed Coverage Report
```bash
pytest --cov=src --cov-report=term-missing tests/
```

### HTML Report
```bash
pytest --cov=src --cov-report=html tests/ && open htmlcov/index.html
```

### Everything: Report + HTML + Threshold
```bash
pytest --cov=src --cov-report=term-missing --cov-report=html --cov-fail-under=80 tests/
```

### Using coverage.py directly
```bash
# Run tests with coverage
coverage run -m pytest tests/

# View report
coverage report

# View HTML
coverage html && open htmlcov/index.html

# Check specific file
coverage report src/calculator.py
```

---

## 📊 Understanding the Reports

### Terminal Report Example

```
Name            Stmts   Miss  Cover   Missing
----------------------------------------------------
src/calculator.py  31      5    84%    36, 41, 46, 51, 56
```

| Column | Meaning |
|--------|---------|
| **Stmts** | Total statements (31 lines of code) |
| **Miss** | Not executed (5 lines) |
| **Cover** | Percentage covered (84%) |
| **Missing** | Line numbers not covered |

### HTML Report Colors

- 🟢 **Green:** Executed by tests
- 🔴 **Red:** NOT executed by tests
- 🟠 **Orange:** Partially executed (some branches)

---

## 🐛 Common Issues & Fixes

### Issue: "No coverage data"
```bash
# Make sure you're in the right directory
cd coverage_example
pwd  # Should show: .../coverage_example

# Then run
pytest --cov=src tests/
```

### Issue: "Import errors"
```bash
# Make sure __init__.py exists in src/
ls src/__init__.py

# Add to PYTHONPATH if needed
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest --cov=src tests/
```

### Issue: "Module not found"
```bash
# Check structure
ls -la src/
# Should show: __init__.py, calculator.py

ls -la tests/
# Should show: __init__.py, test_calculator.py
```

---

## 📝 Exercises

### Exercise 1: Increase Coverage to 95%

1. Run `pytest --cov=src --cov-report=term-missing tests/`
2. See which lines are missing
3. Add tests to cover those lines
4. Rerun until coverage > 95%

**Hint:** Look for error conditions and edge cases

### Exercise 2: Add New Function with Full Coverage

1. Add new function to `src/calculator.py`:
   ```python
   def square_root(n):
       if n < 0:
           raise ValueError("Cannot take sqrt of negative")
       return n ** 0.5
   ```

2. Add tests to `tests/test_calculator.py`:
   ```python
   def test_square_root():
       assert square_root(9) == 3.0

   def test_square_root_negative():
       with pytest.raises(ValueError):
           square_root(-1)
   ```

3. Run coverage - should have 100% for `square_root` 🎉

### Exercise 3: Track Coverage Over Time

```bash
# Day 1: Run and save
pytest --cov=src --cov-report=term-missing tests/ > coverage_day1.txt

# Day 2: After adding more tests
pytest --cov=src --cov-report=term-missing tests/ > coverage_day2.txt

# Compare
diff coverage_day1.txt coverage_day2.txt
```

---

## 🎓 Learning Path

1. ✅ **Run basic tests:** `pytest tests/`
2. ✅ **Add coverage:** `pytest --cov=src tests/`
3. ✅ **See missing lines:** `pytest --cov=src --cov-report=term-missing tests/`
4. ✅ **Generate HTML:** `pytest --cov=src --cov-report=html tests/`
5. ✅ **Write more tests:** Add tests for missing lines
6. ✅ **Set threshold:** `pytest --cov=src --cov-fail-under=80 tests/`
7. ✅ **Use configuration:** Update `.coveragerc` and `pytest.ini`

---

## 🚀 Next Steps

1. **Explore the code:** Look at `src/calculator.py`
2. **Run the examples:** Try each command above
3. **Modify tests:** Add your own test cases
4. **Check the guide:** Read `../code_coverage.md` for detailed info
5. **Practice:** Try the exercises above

---

## 📚 Files Explained

### `src/calculator.py`
Module with math functions (add, subtract, divide, etc.)

### `tests/test_calculator.py`
Tests for calculator functions - intentionally incomplete to show low coverage

### `.coveragerc`
Configuration for coverage.py:
- Which files to measure
- Which lines to exclude
- Minimum coverage requirement (70%)

### `pytest.ini`
Configuration for pytest:
- Where tests are located
- How to run tests
- Test markers

---

## ✨ Pro Tips

1. **Use `--cov-report=html`** to see visual representation
2. **Set `fail_under` threshold** in `.coveragerc` to enforce quality
3. **Add `pragma: no cover`** for lines you don't want to test
4. **Use `--cov-branch`** to test conditional branches
5. **Run coverage in CI/CD pipeline** to maintain quality

---

## 📖 Additional Resources

- **Main Guide:** `../code_coverage.md`
- **Coverage.py Docs:** https://coverage.readthedocs.io/
- **Pytest-cov Docs:** https://pytest-cov.readthedocs.io/

---

**Happy Testing! 🧪**

Now run this to see coverage in action:
```bash
pytest --cov=src --cov-report=html tests/ && open htmlcov/index.html
```
