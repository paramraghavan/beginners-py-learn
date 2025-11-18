To persist a Python dictionary on script shutdown and recover it at startup, use the `pickle` module to serialize the
dictionary. You can catch normal shutdowns (SIGTERM, SIGINT, Ctrl+C) but *cannot* catch `kill -9` (SIGKILL), which
immediately terminates the process and does not trigger any Python exit handlers.

### Serialization and Restoration Example

```python
import pickle
import os
import signal
import sys
import atexit

DICT_PATH = 'state.pickle'
my_dict = {}


def save_state():
    with open(DICT_PATH, 'wb') as f:
        pickle.dump(my_dict, f)


def load_state():
    global my_dict
    if os.path.exists(DICT_PATH):
        with open(DICT_PATH, 'rb') as f:
            my_dict = pickle.load(f)


# Restore dictionary on startup
load_state()


def handle_exit(signum, frame):
    print(f"Received signal {signum}, saving state and exiting.")
    save_state()
    sys.exit(0)


# Register handlers for shutdown signals
signal.signal(signal.SIGINT, handle_exit)  # Ctrl+C
signal.signal(signal.SIGTERM, handle_exit)  # kill <pid>

# Register atexit handler for normal process shutdown
atexit.register(save_state)

# ... your main logic here ...
```

- On script startup, it loads any previously saved dictionary.
- On shutdown (`SIGTERM`, `SIGINT`, `Ctrl+C`, python exit), it dumps the dictionary to a pickle file.
- `kill -9 <pid>` cannot be caught or handled; data loss is possible if used.

### Important Considerations

- Only SIGINT (Ctrl+C) and SIGTERM (kill <pid>) can be caught. SIGKILL(kill -9) can never be caught or handled by any
  Python code
  or signal handler.
- Use `atexit.register(save_state)` to cover clean shutdowns not tracked by signals (e.g., natural script exits).
- For atomic writes and to avoid partial file corruption, consider writing to a temp file and renaming it after success.

### Recovery Example

```python
# To restore on startup, just call load_state()
load_state()  # populates my_dict with previously persisted data
```

Above persists a dictionary across restarts except for hard kills by SIGKILL (`kill -9`).

## pickle.HIGHEST_PROTOCOL

**`protocol=pickle.HIGHEST_PROTOCOL`** in Python’s `pickle.dump()` function ensures the object is serialized using the
most recent (and generally most efficient) pickle protocol available in your Python version.

### What is a pickle protocol?

- A protocol is the format Python uses to serialize objects.
- There are several versions (0, 1, 2, ...), with each newer protocol often:
    - Supporting more data types
    - Producing smaller and faster files
    - Improving compatibility and speed

### What does `pickle.HIGHEST_PROTOCOL` do?

- Instead of specifying a fixed number (e.g., `protocol=3`), `pickle.HIGHEST_PROTOCOL` automatically uses the newest
  protocol supported by your Python interpreter.
- **Pros:**
    - Maximizes serialization speed and efficiency.
    - Ensures you get all improvements from the latest Python release.
- **Cons:**
    - Pickle files created with the highest protocol may not be readable on older Python versions (if you transfer files
      between machines with older Python).

**Example:**

```python
import pickle

# Use highest protocol for best speed/efficiency
pickle.dump(my_dict, file, protocol=pickle.HIGHEST_PROTOCOL)
```

**Summary:**  
Using `pickle.HIGHEST_PROTOCOL` is the recommended way to always get the best pickle performance and capabilities—unless
you need to support very old Python interpreters.

## Data structures supported when saving with pickle

Pickle supports almost all built-in and user-defined data structures, including:

- **Dicts of dicts** (nested dictionaries)
- **List (array) of dicts**
- **2-dimensional lists or arrays** (e.g., `[[1,2],[3,4]]`)
- **Tuples, sets, custom classes**
- Any combination —pickle will recursively serialize the entire structure.

**Examples:**

```python
data1 = {'a': {'b': 1, 'c': 2}, 'd': 3}  # dict of dict
data2 = [{'name': 'Alice'}, {'name': 'Bob'}]  # list of dicts
data3 = [[1, 2], [3, 4]]  # 2D list
data4 = {'arr': [[1, 2], [3, 4]], 'meta': {'x': 5}}  # mixed dict and list
```

**Usage:**
You can call `save_state(your_object)` and `load_state()` for any of the above.

```python
save_state(data1)  # will pickle nested dicts
save_state(data2)  # will pickle list of dicts
save_state(data3)  # will pickle 2D array
```

When you load back, you get your original structure.

**Limitations:**

- _Objects must be picklable_; most built-ins (dict, list, set, tuple, etc.) and custom classes are, but some things (like
  open file handles, sockets, generatos, some C extensions) cannot be pickled.
- Use the same Python version (and object definitions) for serialize/deserialize when using custom classes.

> You can serialize nearly any nested or composite Python data structure with pickle, including dicts of dicts, lists of
dicts, and multidimensional arrays


