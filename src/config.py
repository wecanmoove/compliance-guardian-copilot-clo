"""Application configuration.

Paths are resolved relative to the project root so the app runs correctly
regardless of the current working directory (e.g. when launched by a preview
runner from a different folder).
"""
import os
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

# Project root = parent of the src/ directory containing this file.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
_ENV_FILE = PROJECT_ROOT / ".env"
_SQLITE_PATH = PROJECT_ROOT / "compliance_guardian.db"


class Settings(BaseSettings):
    """App settings from environment variables / .env."""

    # Database — defaults to local SQLite so no external service is required.
    database_url: str = f"sqlite:///{_SQLITE_PATH.as_posix()}"

    # Redis
    redis_url: str = "redis://localhost:6379"

    # API Keys
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None

    # App
    secret_key: str = "dev-secret-change-me"
    debug: bool = True
    environment: str = "development"

    # Storage
    storage_path: str = str(PROJECT_ROOT / "uploads")

    # Server
    port: int = 8000
    host: str = "127.0.0.1"

    model_config = SettingsConfigDict(
        env_file=str(_ENV_FILE),
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
