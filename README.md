# beginners-py-learn
### A Comprehensive Python Learning Resource

> **🎯 NEW: Comprehensive Python Handbook Available!**
>
> Start here: **[📘 Python Handbook](handbook/README.md)** - Complete guide from beginner to advanced
>
> Or jump directly to: **[📗 Master Index & Navigation](handbook/PYTHON_HANDBOOK.md)** - Full table of contents

---

## AI and Coding
- [coding_with_ai.md](quick101/coding_with_ai.md)

## 🚀 Quick Start Paths

### For Complete Beginners
→ **[Quick Start Guide](handbook/PYTHON_HANDBOOK.md#quick-start-guide)** - 12-week structured curriculum
→ **[Python Study Guide](handbook/python-study-guide.md)** - 19 comprehensive chapters

### For Job Interview Preparation
→ **[Interview Prep Supplement ⭐ NEW](handbook/interview-prep-supplement.md)** - 50 problems, system design, behavioral, company-specific
→ **[Interview Preparation Hub](handbook/PYTHON_HANDBOOK.md#-interview-preparation)** - Overview & learning paths
→ **[Quick Reference Cards](handbook/quick-reference-cards.md)** ⭐ - One-page cheatsheets for Python, SQL, Git, Docker, AWS

### By Career Path
→ **[Software Engineer Path](handbook/paths/software-engineer-path.md)** *(coming)* - Web dev, databases, DevOps
→ **[Data Scientist Path](handbook/paths/data-scientist-path.md)** *(coming)* - ML, statistics, visualization
→ **[Data Engineer Path](handbook/paths/data-engineer-path.md)** *(coming)* - ETL, pipelines, cloud
→ **[DevOps Engineer Path](handbook/paths/devops-engineer-path.md)** *(coming)* - Docker, Kubernetes, CI/CD

### Traditional Learning Approach
- [Click here and start with 0-learn_variables.py](src/)
- [Quick 101](quick101)
- [Advanced](src/advance_stuff/readme.md)
- [Quick Review](cheatsheet/quick-review.md)

---

## 📚 Learning Resources

### Core Content
- **[Handbook README](handbook/README.md)** - Welcome & how to use the handbook
- **[Master Handbook Index](handbook/PYTHON_HANDBOOK.md)** - Complete table of contents with all sections
- **[Python Study Guide](handbook/python-study-guide.md)** - 19-chapter comprehensive curriculum

### Specialized Resources
- **[10 Python Features You Should Use](handbook/10_python_features_you_should_be_using.md)** - Write Pythonic code
- **[Threading & Concurrency Guide](handbook/python_threading_locks_guide.md)** - Concurrency essentials
- **[Excel Primer](handbook/excel_primer.md)** - Data work with spreadsheets
- **[Jupyter Notebook Setup](handbook/jupyter-notebook/jupyter_setup_and_tutorial.md)** - Interactive learning
- **[Pandas DataFrame Tutorial](handbook/pandas_dataframe/pandas_dataframe_tutorial.md)** - Data manipulation

### Complementary Topics
- **[Basics of how a program works](src/how-does-a-program-run.md)**

---

## ⚙️ Development Environment Setup

### Choose Your IDE
- **[PyCharm Community Edition](https://www.jetbrains.com/pycharm/download/)**
- **[Visual Studio Code](https://code.visualstudio.com/)**
- **[Spyder](https://www.spyder-ide.org/)**
- **[Environment Setup Guide](python_environment_setup.md)**
- Any text editor (Sublime, Vim, etc.)

### Git & Version Control
- **[GitHub 101](quick101/how-to-git/github-101.md)** - Getting started with GitHub
- **[How to Use GitHub](quick101/how-to-git/how-to-use-github.md)** - Practical workflows
- **[Git Setup & Common Mistakes](simple_git_setup_common_msitakes.md)** - Fix setup issues

---

## 🔧 Code Quality & Tools

### Code Analysis & Formatting
Essential tools for professional Python development:

| Tool | Purpose |
|------|---------|
| **pylint** | Comprehensive code analysis |
| **flake8** | Style guide enforcement |
| **black** | Code formatter (PEP 8) |
| **mypy** | Type checking |
| **autopep8** | PEP 8 style fixes |
| **isort** | Import sorter |
| **bandit** | Security linting |

**[Full Guide: Linter & Code Review](quick101/code_review/linter-misc.md)**

### Security & Vulnerability
- **[Vulnerability Checking](quick101/vulnerability-check.md)** - Scan dependencies for security issues

---

## 📐 Additional Resources

### Math for Computer Science
- [MIT Mathematics for Computer Science](https://courses.csail.mit.edu/6.042/spring18/mcs.pdf)

---

## 📦 Dependency Management

### requirements.txt vs Pipfile

| Feature | requirements.txt | Pipfile |
|---------|------------------|---------|
| Lightweight | ✅ Yes | ❌ No |
| Dev dependencies | ❌ Separate file | ✅ Built-in |
| Lock file | ❌ None | ✅ Pipfile.lock |
| Dependency resolution | ⚠️ Basic | ✅ Advanced |
| Industry adoption | ✅ Very high | ⚠️ Growing |

**Use requirements.txt for:** Simple projects, CI/CD systems, cloud deployments
**Use Pipfile for:** Complex projects, deterministic builds, dev dependency separation

### Quick Commands

**requirements.txt:**
```bash
pip install -r requirements.txt
pip freeze > requirements.txt
```

**pipenv:**
```bash
pipenv install [package]              # Install & update Pipfile
pipenv install --dev pytest           # Install dev dependency
pipenv shell                          # Activate virtual environment
pipenv graph                          # View dependency tree
pipenv lock -r > requirements.txt     # Convert to requirements.txt
pipenv --python 3.10                  # Specify Python version
pipenv --rm                           # Remove virtual environment
```

**Troubleshooting:**
```bash
pipenv lock --clear                   # Clear caches
pipenv lock --verbose                 # Debug resolution issues
pipenv install --upgrade              # Upgrade dependencies
```

### Detailed Guides
- [Complete pipenv documentation](https://pipenv.pypa.io/)
- [Virtual environment setup guide](handbook/python-study-guide.md#chapter-9-python-environment-pip--dependency-management)

---

## Virtual Environment Setup
**[Complete Setup Guide →](handbook/python-study-guide.md#chapter-9-python-environment-pip--dependency-management)**

Quick commands:
```bash
# Create virtual environment
python -m venv .venv

# Activate (Mac/Linux)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate

# Install packages
pip install -r requirements.txt

# Create requirements file
pip freeze > requirements.txt
```

**VS Code Configuration:**
- [Select Python Interpreter](https://code.visualstudio.com/docs/python/environments)
- Use Ctrl+Shift+P → "Python: Select Interpreter"

### Inspect Your Environment
- **[Inspect Local Python Environment](src/advance_stuff/inspect_local_python_env.py)** - View installed packages and settings

---

## 🎓 Python Concepts & Advanced Topics

### Core Python Knowledge
- **[Modules, Packages, Libraries & Frameworks](handbook/python-study-guide.md#chapter-8-modules-packages--imports)** - Understanding Python's organization
- **[Object-Oriented Programming](handbook/python-study-guide.md#chapter-5-object-oriented-programming)** - Classes, inheritance, polymorphism
- **[Variable Access Control](README.md)** - Public, protected, private (conventions)
- **[The `__init__` Method](quick101/init-and-new.md)** - Class initialization explained
- **[The `__name__` Variable](src/advance_stuff/main/main.py)** - Running as main vs import
- **[Sequence Types in Python](src/advance_stuff/pycollections/sequence.md)**

### Advanced Concepts
- **[Abstract Base Classes (ABC)](https://elfi-y.medium.com/inheritance-in-python-with-abstract-base-class-abc-5e3b8e910e5e)** - Creating interfaces
- **[Design Patterns in Python](src/advance_stuff/patterns)** - Decorator, factory, singleton, etc.
- **[Dunder Methods](quick101/dunder-methods/)** - `__add__`, `__str__`, etc.
- **[API Design in Python](src/advance_stuff/apis-how-to/)** - Building good APIs
- **[Python Class Initialization Sequence](src/advance_stuff/class_init_sequence/)**

### Data Structures & Algorithms
- **[Data Structures Overview](https://towardsdatascience.com/which-python-data-structure-should-you-use-fa1edd82946c)** - When to use which
- **[Data Structure Examples](src/advance_stuff/data_structure)** - Implementation examples
- **[Data Structure Textbook](https://doc.lagout.org/science/0_Computer%20Science/2_Algorithms/Data%20Structures%20and%20Algorithms%20using%20Python%20%5BNecaise%202010-12-21%5D.pdf)** - Comprehensive reference

### Databases
- **[Setup Local Databases](src/database/README.md)** - PostgreSQL & MongoDB with Docker
- **[Database Operations Guide ⭐ NEW](handbook/database-operations-guide.md)** - SQL, SQLAlchemy, PostgreSQL, MongoDB, Redis, patterns

### Python Ecosystem
- **[PyPI Package Repository](https://pypi.org/)** - Find & publish packages
- **[How to Build Python Packages](https://github.com/paramraghavan/pkg_example_project#readme)** - Version management & publishing

---

## ⚡ Performance & Profiling

### Code Profiling
**See detailed guide in:** [Chapter 10: Debugging & Profiling](handbook/python-study-guide.md#chapter-10-debugging--profiling)

Quick profiling with cProfile:
```bash
python -m cProfile -o output.pstats your_script.py
```

### Profiling Visualization Tools

| Tool | Command | Purpose |
|------|---------|---------|
| **snakeviz** | `snakeviz output.pstats` | Interactive visualization |
| **gprof2dot** | `gprof2dot -f pstats output.pstats \| dot -Tpng -o graph.png` | Call graph visualization |
| **viztracer** | `viztracer -o result.json script.py && vizviewer result.json` | Real-time trace visualization |

[Profiling Tools Reference](https://medium.com/@narenandu/profiling-and-visualization-tools-in-python-89a46f578989)

### pip install vs python -m pip install

| Command | Use Case |
|---------|----------|
| `pip install package` | Quick, direct installation |
| `python -m pip install package` | **Recommended** - explicit Python version, better with virtual envs |

**Best practice:** Use `python -m pip install` to avoid confusion with multiple Python versions.

### Package Distribution
- **[Convert Python Scripts to Binary](building_binary_files_for_python_scripts.md)** - Create standalone executables
- **[Build & Publish Packages](https://github.com/paramraghavan/pkg_example_project#readme)** - Version management & PyPI

---

## 🛠️ Specialized Topics

### Data Science & ML
- **[ML Workflow Guide ⭐](handbook/ml-workflow-guide.md)** - End-to-end ML projects, model deployment
- Image processing with OpenCV
- TensorFlow & Neural Networks
- D-Tale for data exploration ([docs](https://pypi.org/project/dtale/))

### DevOps & Cloud
- **[Cloud & DevOps Guide ⭐ NEW](handbook/cloud-devops-guide.md)** - Docker, Kubernetes, AWS, CI/CD, GitHub Actions, Infrastructure as Code
- **[CI/CD Pipelines ⭐](handbook/cloud-devops-guide.md#cicd-pipelines)** - GitHub Actions, automation, deployment

### Mobile Development
- [BeeWare](https://docs.beeware.org/) - Python on iOS/Android
- [Kivy](https://kivy.org/) - Python mobile framework
- [ActiveState - Python Mobile Frameworks](https://www.activestate.com/blog/the-best-python-frameworks-for-mobile-development/)

### BI & Analytics
- **[Apache Superset Setup](quick101/apache_superset.md)** - Open-source BI tool
- **[Apache Superset with CSV](quick101/apache_superset_with_csv.md)** - Quick start

---

## 📋 PEP 8 Style Guide

**[Full PEP 8 Guide →](https://peps.python.org/pep-0008/)**

Quick reference:
- **Indentation:** 4 spaces per level
- **Line length:** Max 79 characters (code), 72 (comments)
- **Naming:** `lowercase_with_underscores` for functions, `CapWords` for classes
- **Imports:** Separate lines at top of file
- **Readability:** Simple is better than complex

---

## 📚 Recommended Resources

### Books & Guides
- [Cracking the Coding Interview](http://www.amazon.com/Cracking-Coding-Interview-Programming-Questions/dp/098478280X)
- [Algorithm Fundamentals](http://algs4.cs.princeton.edu/10fundamentals/)
- [Python Tutorial by Akuli](https://github.com/Akuli/python-tutorial)
- [Google's Python Tutorial](https://developers.google.com/edu/python)

### Coding Practice
- **[Leetcode](https://leetcode.com/)** - Algorithm problems
- **[CodeChef](https://www.codechef.com/)** - Competitive programming
- **[Project Euler](http://projecteuler.net/)** - Math & programming problems
- **[High Scalability Blog](http://highscalability.com/blog/category/example)** - System design patterns

### Learning & Big-O
- [Big-O Notation Explained](https://medium.com/@zoebai_70369/big-o-notation-time-and-space-complexity-305a1e301e35)
- [Big-O Examples](https://developerinsider.co/big-o-notation-explained-with-examples/)
- [Big-O Factorial](https://jarednielsen.com/big-o-factorial-time-complexity/)

### Useful Articles
- [Which Data Structure Should You Use?](https://towardsdatascience.com/which-python-data-structure-should-you-use-fa1edd82946c)
- [Python Module vs Package vs Library vs Framework](https://dev.to/lucs1590/python-module-vs-package-vs-library-vs-framework-4i0p)
- [Python 3.9 vs 3.10](https://www.analyticsvidhya.com/blog/2021/08/differences-between-python-3-10-and-python-3-9-which-you-need-to-know)
- [Python Backward Compatibility](https://stackoverflow.com/questions/70467517/how-can-i-know-what-python-versions-can-run-my-code)

---

## 💡 Interesting Topics & Projects

### Image Processing & Restoration
- [Image Enhancement with OpenCV](https://towardsdatascience.com/image-enhancement-techniques-using-opencv-and-python-9191d5c30d45)
- [Pencil Sketch Effect](https://github.com/pythonlessons/background_removal)
- [Neural Style Transfer](https://github.com/omerbsezer/NeuralStyleTransfer#readme)
- [GFPGAN - Face Restoration](https://github.com/TencentARC/GFPGAN)

### System Utilities
- [Computer System Status Monitor](https://github.com/msimms/ComputerStatus)

### Documentation & Diagramming
- **[Markdown](https://www.markdownguide.org/)** - Documentation language
- **[Mermaid & Markdown](https://mermaid.live/)** - Diagrams as code
- **[draw.io](https://get.diagrams.net/)** - Diagramming tool
- **[Excalidraw](https://excalidraw.com/)** - Free whiteboarding
- **[tldraw](https://www.tldraw.com/)** - Sketching tool

### Project Structure
```bash
# View directory tree
brew install tree
tree -I 'dir_to_exclude'
```

---

## 📄 Software Licenses

Quick summary of common licenses:

| License | Type | Key Points |
|---------|------|-----------|
| **MIT, BSD, ISC** | Permissive | "Do whatever you want, don't sue me" |
| **Apache** | Permissive | More specific, includes patent clause |
| **GPL (v2/v3)** | Copyleft | Must share source if distributed |
| **LGPL** | Weak copyleft | More flexible than GPL |
| **AGPL** | Strong copyleft | Must share source even if not distributed |

**[Comprehensive License Guide →](https://www.exygy.com/blog/which-license-should-i-use-mit-vs-apache-vs-gpl)**

---

## 🔍 Python & Backward Compatibility

**Key point:** Python maintains compatibility between minor versions (3.8 → 3.9 → 3.10).

- **Breaking change only:** Python 2 → Python 3 (2020 EOL)
- **Minor breaks possible:** Usually for security, deprecation warnings given
- **Check What's New:** Python documentation for each version release

[Python Compatibility Guide](https://stackoverflow.com/questions/70467517/how-can-i-know-what-python-versions-can-run-my-code)

---

## 🤝 Contributing

Found a bug or have a suggestion? We'd love your help!

1. Fork this repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

[GitHub Repository](https://github.com/paramraghavan/beginners-py-learn)

---

## ❓ Troubleshooting

### Git SSL Certificate Error
```bash
git config --global http.sslBackend schannel
```

### pip Not Found
```bash
# Download get-pip.py
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```

### Interview Preparation
- [MyGreatLearning Python Interview Questions](https://www.mygreatlearning.com/blog/python-interview-questions/)
- [Amazon's Technical Problem Solving](https://www.myamcat.com/amazon-lateral-demo)

---

## 📞 Support

- **Browse this README** - Start with table of contents above
- **Open an issue** - [GitHub Issues](https://github.com/paramraghavan/beginners-py-learn/issues)
- **Read the handbook** - [Complete Python Handbook](handbook/README.md)

---

## ⭐ Quick Links

**Learning:**
- [Python Handbook](handbook/README.md)
- [Python Study Guide](handbook/python-study-guide.md)
- [Quick Reference Cards](handbook/quick-reference-cards.md) ⭐ NEW
- [CS50P (Harvard, Free)](https://cs50.harvard.edu/python/)
- [Python Data Structures](https://docs.python.org/3/tutorial/datastructures.html)

**Interview Prep:**
- [Interview Hub](handbook/PYTHON_HANDBOOK.md#-interview-preparation)
- [Learning Paths](handbook/PYTHON_HANDBOOK.md#-learning-paths-by-role)

**Tools:**
- [Code Review & Linting](quick101/code_review/linter-misc.md)
- [Git & GitHub](quick101/how-to-git/)
- [Vulnerability Checking](quick101/vulnerability-check.md)

---

**Last Updated:** May 2026 | **License:** MIT | **Community Project**
