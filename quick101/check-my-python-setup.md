# Check my python setup

- python -m site
- python -m site --user-site
- pip config list
- pip show <package>
- Check python being used by the current python console/env
```python
import sys
print(sys.executable)
```
- [env.md](env.md)
- [pipenv.md](pipenv.md)

## To list all Python installations on your PC, you can try the following methods:

- Using the command prompt or terminal:

   **On Windows:**
   ```
   where python
   ```

   **On macOS or Linux:**
   ```
   which -a python
   which -a python3
   ```
   These commands will show the paths of Python executables in your system PATH.

2. Check common installation directories:
   On Windows, look in:
   - C:\Python*
   - C:\Program Files\Python*
   - C:\Users\YourUsername\AppData\Local\Programs\Python

   On macOS or Linux, check:
   - /usr/bin/python*
   - /usr/local/bin/python*
   - /opt/homebrew/bin/python* (for Homebrew installations on macOS)

- Use the `py` launcher (Windows only):
   ```
   py -0
   ```
   This will list all Python versions registered with the py launcher.

- Check your system's package manager:

   On macOS with Homebrew:
   ```
   brew list | grep python
   ```

   On Linux (Ubuntu/Debian):
   ```
   dpkg --list | grep python
   ```

- Use a PowerShell script (Windows):

   ```powershell
   Get-ChildItem -Path C:\ -Include python.exe -File -Recurse -ErrorAction SilentlyContinue
   ```

   This will search for all `python.exe` files on your C drive.

## List/Print the dependencies for installed packages
```shell
# Method 1: Using pip show
pip show package_name
pip show package_name | grep Requires: --> direct dependencies
pip show package_name | grep Required-by: --> packages that depend on this one
# Example:
pip show requests   # Shows metadata including dependencies

# Method 2: Using pipdeptree
pip install pipdeptree
pipdeptree -p package_name  # Shows dependency tree for specific package
```

## List/Print the dependencies for not yet installed packages
```shell
# Method 1: Using pip show --no-deps
pip download package_name --no-deps
pip show --no-deps package_name.whl

# Method 2: Using yolk3k
pip install yolk3k
yolk -D package_name

# Method 3: Check PyPI website
# Visit https://pypi.org/project/package_name/

# Method 4: Using pip-tools
pip install pip-tools
pip-compile --no-annotate --no-emit-index-url <(echo "package_name")
```


>For installed packages: **pip show package_name**

>For uninstalled packages: 
>  Check the PyPI website or
>  use pip download followed by pip show


## Custom script
- Checks if the package is installed before attempting analysis
- Option to automatically install missing packages
- Recursively install dependencies if needed
- Direct dependencies (immediately required by the package)
- All dependencies (including transitive/nested dependencies)
- 