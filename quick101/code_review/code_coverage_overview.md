# Code Coverage Guide - Overview

You now have **comprehensive code coverage documentation** and a **working example** to learn from.

---

## 📂 What You Have

### 1. **code_coverage.md** (Main Guide)
**Location:** `/quick101/code_review/code_coverage.md`

**Contains:**
- What is code coverage?
- Why it matters
- Tools available (coverage.py, pytest-cov)
- Complete step-by-step setup
- Running coverage
- Analyzing results
- Best practices
- Advanced usage
- Real-world workflows
- Common issues & solutions

**Use for:** Deep learning, reference material

---

### 2. **coverage_example/** (Working Project)
**Location:** `/quick101/code_review/coverage_example/`

**Contains:**
```
src/
  ├── __init__.py
  └── calculator.py          ← Module to test
tests/
  ├── __init__.py
  └── test_calculator.py     ← Tests (intentionally incomplete)
.coveragerc                   ← Coverage config
pytest.ini                    ← Pytest config
requirements.txt              ← Dependencies
QUICK_START.md                ← Step-by-step tutorial
```

**Use for:** Hands-on practice, learning by doing

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Navigate to example
```bash
cd quick101/code_review/coverage_example
```

### Step 2: Install dependencies
```bash
pip install -r requirements.txt
# Or: pip install pytest pytest-cov coverage
```

### Step 3: Run tests
```bash
pytest tests/
```

### Step 4: Check coverage
```bash
pytest --cov=src --cov-report=term-missing tests/
```

### Step 5: View HTML report
```bash
pytest --cov=src --cov-report=html tests/
open htmlcov/index.html
```

**Done!** You've just measured code coverage. 🎉

---

## 📊 What You'll See

### Terminal Output
```
Name                 Stmts   Miss  Cover   Missing
--------------------------------------------------
src/calculator.py       31      5    84%   36, 41, 46, 51, 56
--------------------------------------------------
TOTAL                   31      5    84%
```

**Meaning:** 84% of code is tested. Lines 36, 41, 46, 51, 56 are untested.

### HTML Report
Open `htmlcov/index.html` to see:
- 🟢 Green lines: Tested
- 🔴 Red lines: Not tested
- 🟠 Orange lines: Partially tested

---

## 📚 Learning Path

### Beginner
1. Read "What is Code Coverage?" in `code_coverage.md`
2. Follow `coverage_example/QUICK_START.md` steps 1-5
3. Run the example commands

### Intermediate
1. Read "Best Practices" section
2. Modify tests in `coverage_example/tests/test_calculator.py`
3. Add new tests to increase coverage
4. Try all the one-liners

### Advanced
1. Read "Advanced Usage" section
2. Configure `.coveragerc` for your needs
3. Set up in CI/CD pipeline
4. Track coverage over time

---

## 🎯 Key Commands

### Simple Coverage
```bash
pytest --cov=src tests/
```

### With Missing Lines
```bash
pytest --cov=src --cov-report=term-missing tests/
```

### HTML Report
```bash
pytest --cov=src --cov-report=html tests/
```

### With Threshold (Fail if < 80%)
```bash
pytest --cov=src --cov-fail-under=80 tests/
```

### Everything Combined
```bash
pytest \
  --cov=src \
  --cov-report=term-missing \
  --cov-report=html \
  --cov-fail-under=80 \
  tests/
```

---

## ✨ What to Practice

### Exercise 1: Run the Example
```bash
cd coverage_example
pytest --cov=src --cov-report=html tests/
open htmlcov/index.html
```
**Goal:** Understand how to read coverage reports

### Exercise 2: Add Tests
Edit `coverage_example/tests/test_calculator.py` to add tests for:
- Division by zero error
- Power with negative exponent
- Absolute value edge cases

**Goal:** See coverage percentage increase

### Exercise 3: Set Threshold
```bash
pytest --cov=src --cov-fail-under=85 tests/
```
**Goal:** Use coverage as quality gate

### Exercise 4: Generate HTML
```bash
pytest --cov=src --cov-report=html tests/ && open htmlcov/index.html
```
**Goal:** View detailed visual report

---

## 🔑 Key Concepts

### Coverage Metrics
| Metric | What It Measures |
|--------|------------------|
| Line Coverage | % of lines executed |
| Branch Coverage | % of if/else branches taken |
| Function Coverage | % of functions called |

### Coverage Targets
- **Good:** 80%
- **Excellent:** 90%+
- **Unrealistic:** 100%

### Why It Matters
- ✓ Finds untested code
- ✓ Reduces bugs
- ✓ Improves quality
- ✓ Prevents regressions
- ✓ Builds confidence

---

## 🛠️ Tools Used

### coverage.py
- **Purpose:** Measure Python code coverage
- **Command:** `coverage run`, `coverage report`, `coverage html`

### pytest-cov
- **Purpose:** Coverage plugin for pytest
- **Command:** `pytest --cov=...`
- **Advantage:** Simpler, integrates with pytest

### Configuration Files
- **`.coveragerc`:** Coverage settings
- **`pytest.ini`:** Pytest settings

---

## 📖 Document Structure

### code_coverage.md Sections
1. What is Code Coverage? (concept)
2. Why Code Coverage Matters (benefits)
3. Tools Available (options)
4. Quick Start (5 minutes)
5. Step-by-Step Setup (detailed)
6. Running Coverage (commands)
7. Analyzing Results (interpretation)
8. Best Practices (advice)
9. Advanced Usage (power user)

### coverage_example Directory
1. Real, working Python code
2. Tests with intentional gaps
3. Configuration files
4. Requirements file
5. Tutorial (QUICK_START.md)

---

## 🎓 Next Steps

1. **Read:** Open `code_coverage.md` and read sections 1-3
2. **Practice:** Follow `coverage_example/QUICK_START.md`
3. **Experiment:** Modify the example code and tests
4. **Learn:** Read "Best Practices" section
5. **Apply:** Use coverage in your own projects

---

## 💡 Pro Tips

✓ **Start Simple:** Test one module completely first

✓ **Use HTML Reports:** Easier to spot untested code

✓ **Set Threshold:** `--cov-fail-under=80` enforces quality

✓ **Test Edge Cases:** Error conditions are often missed

✓ **Automate:** Add coverage to CI/CD pipeline

✓ **Iterate:** Improve coverage gradually, not all at once

---

## 🐛 Troubleshooting

**"No coverage data"**
```bash
# Make sure you're in the right directory
cd coverage_example
# Then run the command
```

**"Module not found"**
```bash
# Make sure __init__.py exists
touch src/__init__.py
touch tests/__init__.py
```

**"Import error"**
```bash
# Add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

**See more issues:** Check "Common Issues & Solutions" in `code_coverage.md`

---

## 📞 Need Help?

### For Concepts
→ Read `code_coverage.md` sections "What is Code Coverage?" and "Why Code Coverage Matters"

### For Setup
→ Follow `coverage_example/QUICK_START.md` step by step

### For Commands
→ Check "Key Commands" section above or "Running Coverage" in `code_coverage.md`

### For Best Practices
→ See "Best Practices" in `code_coverage.md`

### For Advanced Topics
→ See "Advanced Usage" in `code_coverage.md`

---

## ✅ Checklist

- [ ] Read "What is Code Coverage?" section
- [ ] Navigate to `coverage_example/`
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Run tests: `pytest tests/`
- [ ] Run coverage: `pytest --cov=src tests/`
- [ ] View HTML: `pytest --cov=src --cov-report=html tests/` + open report
- [ ] Read "Analyzing Results" section
- [ ] Add more tests to improve coverage
- [ ] Rerun coverage to see improvement
- [ ] Read "Best Practices" section
- [ ] Try all the one-liner commands
- [ ] Apply to your own project

---

## 🎯 Your Code Coverage Learning Journey

**Phase 1: Understanding (Today)**
- Learn what code coverage is
- Understand why it matters
- See it in action with the example

**Phase 2: Practice (This Week)**
- Run coverage on the example project
- Add tests to increase coverage
- Generate and analyze reports

**Phase 3: Mastery (This Month)**
- Apply to your own projects
- Set coverage thresholds
- Integrate into CI/CD

**Phase 4: Excellence (Ongoing)**
- Maintain high coverage
- Review untested code regularly
- Share knowledge with team

---

## 🚀 Ready to Start?

### Quickest Path (15 minutes)
```bash
cd quick101/code_review/coverage_example

# Install
pip install -r requirements.txt

# Run
pytest --cov=src --cov-report=html tests/

# View
open htmlcov/index.html
```

### Complete Path (1 hour)
1. Read `code_coverage.md` sections 1-3
2. Follow `coverage_example/QUICK_START.md` completely
3. Do Exercise 1 & 2
4. Read "Best Practices"

### Deep Learning (2-3 hours)
1. Read entire `code_coverage.md`
2. Complete all exercises in `coverage_example/QUICK_START.md`
3. Apply to your own project
4. Read "Advanced Usage"

---

**Choose your path and start learning! 🚀**

Questions? Check the FAQ sections in each document.

Happy testing! 🧪
