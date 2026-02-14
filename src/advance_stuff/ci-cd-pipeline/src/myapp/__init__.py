"""
MyApp - Sample Python Application

A demonstration application with full CI/CD pipeline,
including an ETL (Extract, Transform, Load) framework.
"""

from myapp.main import AppConfig, calculate_sum, get_version, greet, process_data

__version__ = "0.1.0"
__all__ = [
    "AppConfig",
    "calculate_sum",
    "get_version",
    "greet",
    "process_data",
]

# ETL module is available via: from myapp.etl import ...
