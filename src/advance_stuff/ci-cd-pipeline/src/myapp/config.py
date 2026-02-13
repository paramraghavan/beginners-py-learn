"""
Application Configuration

Centralized configuration management using Pydantic settings.
Supports environment variables and .env files.
"""

import os
from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = Field(default="TaskFlow API", description="Application name")
    app_version: str = Field(default="1.0.0", description="Application version")
    debug: bool = Field(default=False, description="Debug mode")
    environment: Literal["development", "staging", "production"] = Field(
        default="development", description="Environment name"
    )

    # Server
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, description="Server port")
    workers: int = Field(default=1, description="Number of workers")

    # Database
    database_url: str = Field(
        default="sqlite:///./taskflow.db", description="Database connection URL"
    )
    database_echo: bool = Field(default=False, description="Echo SQL queries")

    # Security
    secret_key: str = Field(
        default="change-me-in-production-use-strong-secret-key",
        description="Secret key for JWT",
    )
    access_token_expire_minutes: int = Field(
        default=30, description="Access token expiration in minutes"
    )
    algorithm: str = Field(default="HS256", description="JWT algorithm")

    # API
    api_prefix: str = Field(default="/api/v1", description="API prefix")
    allowed_origins: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        description="CORS allowed origins",
    )

    # Logging
    log_level: str = Field(default="INFO", description="Log level")
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log format",
    )

    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.environment == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.environment == "development"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Convenience access
settings = get_settings()
