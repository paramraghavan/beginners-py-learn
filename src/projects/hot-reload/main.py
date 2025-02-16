import json
import importlib
import time
from pathlib import Path
from typing import Dict, Any
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class ConfigHandler(FileSystemEventHandler):
    def __init__(self, config_path: str, callback):
        self.config_path = Path(config_path)
        self.callback = callback
        self.last_modified = self.config_path.stat().st_mtime

    def on_modified(self, event):
        if Path(event.src_path) == self.config_path:
            current_modified = self.config_path.stat().st_mtime
            if current_modified > self.last_modified:
                self.last_modified = current_modified
                self.callback()


class ModuleHandler(FileSystemEventHandler):
    def __init__(self, module_path: str, callback):
        self.module_path = Path(module_path)
        self.callback = callback
        self.last_modified = self.module_path.stat().st_mtime

    def on_modified(self, event):
        if Path(event.src_path) == self.module_path:
            current_modified = self.module_path.stat().st_mtime
            if current_modified > self.last_modified:
                self.last_modified = current_modified
                self.callback()


class HotReloader:
    def __init__(self):
        self.config: Dict[str, Any] = {}
        self.custom_module = None
        self.observer = Observer()

    def load_config(self, config_path: str) -> None:
        """Load configuration from JSON file"""
        with open(config_path, 'r') as f:
            self.config = json.load(f)
            print(f"Configuration loaded: {self.config}")

    def load_module(self, module_name: str) -> None:
        """Load or reload a Python module"""
        try:
            if self.custom_module is None:
                self.custom_module = importlib.import_module(module_name)
            else:
                self.custom_module = importlib.reload(self.custom_module)
            print(f"Module {module_name} loaded successfully")
        except ImportError as e:
            print(f"Error loading module {module_name}: {e}")

    def watch_config(self, config_path: str) -> None:
        """Set up config file watching"""
        handler = ConfigHandler(config_path, lambda: self.load_config(config_path))
        self.observer.schedule(handler, Path(config_path).parent, recursive=False)

    def watch_module(self, module_path: str, module_name: str) -> None:
        """Set up module file watching"""
        handler = ModuleHandler(module_path, lambda: self.load_module(module_name))
        self.observer.schedule(handler, Path(module_path).parent, recursive=False)

    def start(self) -> None:
        """Start the file watching"""
        self.observer.start()

    def stop(self) -> None:
        """Stop the file watching"""
        self.observer.stop()
        self.observer.join()


# Example usage
def main():
    # Initialize the hot reloader
    reloader = HotReloader()

    # Initial loading of config and module
    config_path = "config.json"
    module_path = "custom_module.py"
    module_name = "custom_module"

    reloader.load_config(config_path)
    reloader.load_module(module_name)

    # Set up file watching
    reloader.watch_config(config_path)
    reloader.watch_module(module_path, module_name)

    # Start the observer
    reloader.start()

    try:
        # Main program loop
        while True:
            # Your main program logic here
            print("Current config:", reloader.config)
            if reloader.custom_module:
                reloader.custom_module.do_something()
            time.sleep(5)  # Wait for 5 seconds before next iteration
    except KeyboardInterrupt:
        reloader.stop()


if __name__ == "__main__":
    main()
