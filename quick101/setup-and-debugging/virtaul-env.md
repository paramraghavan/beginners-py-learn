Here are the basic steps using Python’s built‑in **venv** module.

## 1. Check your Python command

In a terminal or command prompt, run one of:

- `python --version`
- `python3 --version`

Use whichever command works on your system in the following steps.

## 2. Go to your project folder

Change into your project directory:

- `cd /path/to/your/project` (macOS/Linux)

## 3. Create the virtual environment

Run:

- `python -m venv venv`  
  or, if your system uses `python3`:
- `python3 -m venv venv`

This creates a `venv` folder in your project containing an isolated Python and pip.

## 4. Activate the virtual environment

Use the command for your OS:

- Windows (cmd):
    - `venv\Scripts\activate`
- Windows (PowerShell):
    - `venv\Scripts\Activate.ps1`
- macOS/Linux:
    - `source venv/bin/activate`

Your prompt should now start with `(venv)`.

## 5. Install packages inside it

With the env active, install packages as usual:

- `pip install requests`
- `pip install -r requirements.txt`

These installs stay isolated in the `venv` directory.

## 6. Deactivate when done
When you are finished:
- `deactivate`

## Typical venv use case

It is good to always use a virtual environment because it isolates each project’s dependencies, avoids version
conflicts, and keeps your global Python installation clean and stable.

* When different projects need different versions of the same package (e.g., one needs Django 3, another Django 4).
* When you want to avoid polluting or breaking the system/global Python with project‑specific libraries.
* When collaborating and you want reproducible installs via requirements.txt (others create a venv and pip install -r
  requirements.txt).
* When testing your project against multiple Python versions or dependency sets by creating multiple isolated envs (
  e.g., .venv-py3.10, .venv-py3.11).
* When you lack admin/root rights but need to pip install packages locally for your user or project directory.
* you need to run One‑off throwaway scripts u
