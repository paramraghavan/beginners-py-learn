Create a singleton class that reads a YAML configuration file and provides access to its values through
static methods.

1. **Singleton Pattern**: The class ensures only one instance exists using the Thread-safe singleton pattern `__new__` method.
2. **Static Access**: Use `ConfigManager.get_value()` to access values without creating an instance.
