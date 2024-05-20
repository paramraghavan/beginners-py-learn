```python
# shared_state.py
def init_global_dict():
    global shared_dict
    shared_dict = {}

def add_to_dict(key, value):
    global shared_dict
    shared_dict[key] = value

def get_from_dict(key):
    global shared_dict
    return shared_dict.get(key)

# package1/module1.py
from shared_state import add_to_dict, init_global_dict

init_global_dict()
add_to_dict('key1', 'value1')

# package2/module2.py
from shared_state import get_from_dict

print(get_from_dict('key1'))  # Output: value1

```