# beginners-py-learn

Python lessons, exercises, and practical examples—from basic syntax to web development, data work, and deployment.

## Start Here

| Your goal | Start with |
| --- | --- |
| Learn Python step by step | [Python Study Guide](handbook/python-study-guide.md) |
| Browse the curriculum | [Handbook Index](handbook/PYTHON_HANDBOOK.md) |
| Practice with code | [Numbered lessons](src/) and [exercises](src/exercises/) |
| Look up syntax quickly | [Quick Reference Cards](handbook/quick-reference-cards.md) |
| Prepare for interviews | [Interview Preparation](handbook/interview-prep-supplement.md) |
| Build something | [Capstone Projects](handbook/projects/README.md) |

New to programming? Follow the study guide, try the examples, and then work through the exercises. The numbered scripts in `src/` provide additional practice; some include error demonstrations, so read the comments and run them in small sections.

## Run an Example

Install Python 3 and Git, then clone the repository:

```bash
git clone https://github.com/paramraghavan/beginners-py-learn.git
cd beginners-py-learn
```

Create and activate a virtual environment using the commands for your platform.

**macOS / Linux (bash or zsh)**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (Command Prompt)**

```bat
python -m venv .venv
.venv\Scripts\activate.bat
```

Run this loops example from the repository root:

```bash
python src/1-learn_loop.py
```

This example needs no third-party packages. Other examples may need additional packages, data files, or services; follow the instructions beside the example you choose. The [ten-feature guide](handbook/10_python_features_you_should_be_using.md) requires Python 3.10 or later; older examples and their dependencies may have different requirements.

The root [requirements.txt](requirements.txt) contains older pinned packages for several examples. Install dependencies for the example you are working on rather than treating that file as a prerequisite for the whole repository.

For more setup help, see [Jupyter setup](python_environment_setup.md), [Conda environments](setup_conda_env.md), or the official [virtual environment guide](https://docs.python.org/3/library/venv.html).

## Explore by Topic

| Topic | Guides and examples |
| --- | --- |
| Python fundamentals | [Study Guide](handbook/python-study-guide.md), [beginner cheatsheet](cheatsheet/python-beginner-cheatsheet.md) |
| Classes and Python features | [Object-oriented basics](quick101/ooo-basics.md), [ten useful features](handbook/10_python_features_you_should_be_using.md), [advanced examples](src/advance_stuff/) |
| Data structures and algorithms | [DSA notes](dsa/data-structures-algorithms.md), [implementation examples](src/advance_stuff/data_structure/) |
| Concurrency | [Threading and Locks](handbook/python_threading_locks_guide.md) |
| Web development | [Web Development Guide](handbook/web-development-guide.md), [Flask examples](src/pyflask/README.md) |
| Databases | [Database Operations](handbook/database-operations-guide.md), [local database setup](src/database/README.md) |
| Data analysis and ML | [pandas tutorial](handbook/pandas_dataframe/pandas_dataframe_tutorial.md), [ML Workflow](handbook/ml-workflow-guide.md), [image processing](src/image_processing/README.md) |
| Testing and code quality | [Code Review and Linting](quick101/code_review/linter-misc.md), [testing guide](quick101/code_review/functional_testing_guide.md) |
| Security | [Security Best Practices](handbook/security-best-practices.md), [dependency checks](quick101/vulnerability-check.md) |
| Cloud and DevOps | [Cloud and DevOps Guide](handbook/cloud-devops-guide.md) |
| Git and developer tools | [GitHub 101](quick101/how-to-git/github-101.md), [PyCharm to VS Code](pycharm_to_vscode_guide.md), [Pipenv notes](quick101/pipenv.md) |
| Coding with AI | [AI coding notes](quick101/coding_with_ai.md) |

### Learning Paths

Once you know the basics, choose a role-focused curriculum:

- [Software Engineer](handbook/paths/software-engineer-path.md)
- [Data Scientist](handbook/paths/data-scientist-path.md)
- [Data Engineer](handbook/paths/data-engineer-path.md)
- [DevOps Engineer](handbook/paths/devops-engineer-path.md)

## Repository Map

| Folder | Contents |
| --- | --- |
| [`handbook/`](handbook/README.md) | Study guide, topic guides, learning paths, and capstone projects |
| [`src/`](src/) | Numbered lessons, exercises, and application examples |
| [`quick101/`](quick101/) | Short explanations, tooling notes, and development workflows |
| [`cheatsheet/`](cheatsheet/) | Python and role-specific reference sheets |
| [`dsa/`](dsa/) | Data structures and algorithms material |
| [`security_scanner/`](security_scanner/README.md) | Security scanner example and documentation |

> Licensed under the [MIT License](LICENSE).
