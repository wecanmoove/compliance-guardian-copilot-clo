"""Application configuration."""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """App settings from environment variables."""
    
    # Database
    database_url: str = "postgresql://compliance_user:compliance_pass@localhost:5432/compliance_guardian"
    
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
    storage_path: str = "./uploads"
    
    # Server
    port: int = 8000
    host: str = "0.0.0.0"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
