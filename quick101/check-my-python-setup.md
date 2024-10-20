# Check my python setup

- python -m site
- python -m site --user-site
- pip config list
- pip show <package>
- Check python bing used by the current python consol/env
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
