import yaml
from typing import Any, Optional
from pathlib import Path


class ConfigManager:
    _instance: Optional['ConfigManager'] = None
    _config: dict = {}

    def __new__(cls) -> 'ConfigManager':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        # Only load config if it hasn't been loaded already
        if not self._config:
            self._load_config()

    def _load_config(self, config_path: str = "config.yaml") -> None:
        """
        Load configuration from YAML file

        Args:
            config_path: Path to the YAML configuration file
        """
        try:
            with open(config_path, 'r') as file:
                self._config = yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found at {config_path}")
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML configuration: {e}")

    @classmethod
    def get_value(cls, key: str, default: Any = None) -> Any:
        """
        Get a configuration value by key

        Args:
            key: The configuration key (supports dot notation for nested keys)
            default: Default value if key is not found

        Returns:
            The configuration value if found, otherwise the default value
        """
        if cls._instance is None:
            cls._instance = cls()

        # Handle nested keys using dot notation
        keys = key.split('.')
        value = cls._instance._config

        for k in keys:
            try:
                value = value[k]
            except (KeyError, TypeError):
                return default

        return value

    @classmethod
    def reload_config(cls, config_path: str = "config.yaml") -> None:
        """
        Reload the configuration from file

        Args:
            config_path: Path to the YAML configuration file
        """
        if cls._instance is None:
            cls._instance = cls()
        cls._instance._load_config(config_path)


# Example usage:
if __name__ == "__main__":
    # Example configuration file (config.yaml):
    """
    database:
      host: localhost
      port: 5432
      name: mydb
    api:
      url: https://api.example.com
      timeout: 30
    """

    # Get configuration values
    db_host = ConfigManager.get_value('database.host')
    db_port = ConfigManager.get_value('database.port')
    api_timeout = ConfigManager.get_value('api.timeout')

    # Get value with default
    debug_mode = ConfigManager.get_value('debug', False)

    # Reload configuration if needed
    ConfigManager.reload_config()

    print(f"Database Host: {db_host}")
    print(f"Database Port: {db_port}")
    print(f"API Timeout: {api_timeout}")
    print(f"Debug Mode: {debug_mode}")
