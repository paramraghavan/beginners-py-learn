Here is a demo Python project example that integrates automated testing and deployment in a simple DevOps workflow.

***

### Overview

- Use a sample Python application (e.g., a calculator module).
- Write unit tests using `unittest`.
- Use a Python script to run tests automatically.
- If tests pass, deploy by creating a Docker container image and pushing it to a Docker registry.
- This demo integrates testing and deployment steps typically found in a DevOps pipeline.

***

### Step 1: Sample Python Application - `calculator.py`

```python
def add(a, b):
    return a + b


def subtract(a, b):
    return a - b
```

***

### Step 2: Unit Tests - `test_calculator.py`

```python
import unittest
import calculator


class TestCalculator(unittest.TestCase):

    def test_add(self):
        self.assertEqual(calculator.add(4, 5), 9)
        self.assertEqual(calculator.add(-1, 1), 0)

    def test_subtract(self):
        self.assertEqual(calculator.subtract(10, 5), 5)
        self.assertEqual(calculator.subtract(2, 2), 0)


if __name__ == '__main__':
    unittest.main()
```

***

### Step 3: DevOps Integration Script - `ci_cd.py`

This script will:

- Run the tests.
- If tests pass, build a Docker image and push it to a Docker registry.
- see Notes below for how unittest/discover work
```python
import subprocess
import sys


def run_tests():
    print("Running tests...")
    result = subprocess.run([sys.executable, '-m', 'unittest', 'discover'], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print("Tests failed.")
        return False
    print("Tests passed.")
    return True


def build_and_push_docker_image():
    print("Building Docker image...")
    # Replace with your own image name and tag
    image_name = "yourdockerhubusername/calculator-demo:latest"
    build_cmd = ["docker", "build", "-t", image_name, "."]
    push_cmd = ["docker", "push", image_name]

    if subprocess.run(build_cmd).returncode != 0:
        print("Docker build failed.")
        return False
    print("Docker image built successfully.")

    if subprocess.run(push_cmd).returncode != 0:
        print("Docker push failed.")
        return False
    print("Docker image pushed successfully.")
    return True


if __name__ == "__main__":
    if run_tests():
        build_and_push_docker_image()
    else:
        print("Deployment aborted due to failed tests.")
```

***

### Step 4: Dockerfile

Create a `Dockerfile` to containerize the app:

```
FROM python:3.10-slim

WORKDIR /app

COPY calculator.py .

CMD ["python3", "-c", "import calculator; print('Calculator module ready to use')"]
```

***

### How to Run

1. Write your app code in `calculator.py`.
2. Write tests in `test_calculator.py`.
3. Build and test with:

```bash
python ci_cd.py
```

This will run tests first. If all tests pass, it will build and push your Docker image.

***

This demo covers the continuous integration (testing) and continuous deployment (Docker build and push) parts of a
DevOps pipeline using Python automation. It can be extended with more complex tests, other deployment targets, or
integrated into CI/CD tools like Jenkins, GitHub Actions, or GitLab CI.

## **Notes**
The `unittest discover` command in Python is used for automatic test discovery and execution. It searches the current
directory and its subdirectories for test files that match a specific pattern (default is `test*.py`), loads all found
test cases, groups them into a test suite, and then runs them.

Key points about `unittest discover`:

- It begins discovery from the current directory by default, recursively searching for test modules.
- Test files must be named to match a pattern (default: files starting with `test`).
- It imports the discovered test modules and collects all `unittest.TestCase` subclasses.
- You can customize discovery with options:
    - `-s` or `--start-directory` to specify the directory to start discovery.
    - `-p` or `--pattern` to specify the filename pattern for test files.
    - `-t` or `--top-level-directory` to specify the top-level directory of the project.
- Running `python -m unittest discover` is equivalent to running `python -m unittest` directly.
- Common usage example:
  ```
  python -m unittest discover -s tests -p '*_test.py'
  ```
  This will discover and run all tests in the `tests` directory matching `*_test.py`.

This command is particularly useful for CI/CD pipelines because it automates the process of finding and executing all
tests without manually specifying them, supporting continuous integration practices.[1][4][7]

***

Summary for your context:
When you run `subprocess.run([sys.executable, '-m', 'unittest', 'discover'])` in Python, it executes this automated test
discovery and runs all tests found in your project folder tree, capturing results for use in your automation script.
This enables automated testing as part of a DevOps pipeline.

>sys.executable ??
```python
result = subprocess.run([sys.executable, '-m', 'unittest', 'discover'], capture_output=True, text=True)
```

does the following:
- It starts a new process to run the command `python -m unittest discover`, which tells Python's built-in `unittest` framework to automatically find and run all test cases in the project using test discovery.[2]
- `sys.executable` ensures the same Python interpreter as the running script is used, in my case it is **'/Applications/Xcode.app/Contents/Developer/usr/bin/python3'**
- `capture_output=True` collects anything printed to standard output or error by the test process so your script can use or display it.
- `text=True` means the output will be captured as a string, not bytes.
- The result object includes the status (if tests passed or failed) and the text output of the test run.
