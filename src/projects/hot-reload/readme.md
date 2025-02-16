A program that demonstrates how to reload configurations and modules dynamically without
restarting the program. 

To use this program, you'll need to set up two additional files:

1. `config.json`:

```json
{
  "setting1": "value1",
  "setting2": "value2"
}
```

2. `custom_module.py`:

```python
def do_something():
    print("Doing something in custom module")
```

This implementation provides:

1. Hot reloading of configuration:
    - Uses watchdog to monitor the config file for changes
    - Automatically reloads when the config file is modified
    - Thread-safe configuration updates

2. Hot reloading of modules:
    - Monitors Python module files for changes
    - Uses importlib.reload() to update module code
    - Maintains module state between reloads

3. Independent operation:
    - Config and module reloading are handled separately
    - Each has its own file system event handler
    - Changes to one don't affect the other

To use this system:

1. Install required package:

```bash
pip install watchdog
```

2. Run the program and try:
    - Modifying config.json to see configuration updates
    - Modifying custom_module.py to see module updates
    - Both will be picked up automatically without restart

3. Setup

**Physical file path to the module**

**Import-style module name (without .py)**
module_name = "custom_module"     # This is how Python imports it
Let me expand this with more detailed examples:
pythonCopy# Example 1: Basic Module Structure
```
Project Structure:
/my_project
    └── main.py
    └── custom_module.py
```

**In main.py**
```python
module_path = "custom_module.py"      # File system path
module_name = "custom_module"         # Import name
```

**Example 2: Module in Subdirectory**
```
Project Structure:
/my_project
    └── main.py
    └── modules/
        └── custom_module.py
```

**In main.py**
```python
module_path = "modules/custom_module.py"  # File system path
module_name = "modules.custom_module"     # Import name with dots
```
