# pickle my class
We can use pickle to save and restore the state of custom classes in Python.

Pickle serializes not only built-in data structures (like dicts, lists, arrays), but also instances of user-defined
classes—provided the class (and its members) are _picklable_.

### Example: Pickling a Custom Class

```python
class MyClass:
    def __init__(self, value):
        self.value = value
        self.data = [1, 2, 3]


instance = MyClass(42)

# Save to file
with open('obj.pickle', 'wb') as f:
    pickle.dump(instance, f, protocol=pickle.HIGHEST_PROTOCOL)

# Load from file
with open('obj.pickle', 'rb') as f:
    loaded_instance = pickle.load(f)

print(loaded_instance.value)  # Output: 42
print(loaded_instance.data)  # Output: [1, 2, 3]
```

### When does pickle work with custom classes?

- If your class is defined in the top-level scope of a module (_not_ inside another function/class).
- All instance attributes are themselves picklable (lists, dicts, primitives, or other picklable objects).
- If using custom `__getstate__` and `__setstate__`, these can control how the object’s state is
  serialized/deserialized (for advanced use cases).

### **Limitations**

- Pickle won’t work for:
    - Instances referencing things like open files, sockets, threads, or lambda functions.
    - Classes defined inside functions, closures, or with certain `__slots__` restrictions.
- If you refactor your class code after pickling, old pickles _may_ fail to load if the class definition changes.


> You can safely save and restore most custom Python class instances using pickle, as long as the members are picklable
and the class is defined properly. **Pickle supports nested, complex, and user-defined types, making it very flexible
for application state persistence.**