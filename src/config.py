from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # App
    APP_ENV: str = "development"
    APP_NAME: str = "Compliance Guardian Copilot"
    APP_VERSION: str = "0.1.0"
    SECRET_KEY: str = "dev-secret-key-change-in-prod"
    
    # Database
    DATABASE_URL: str = "postgresql://cgc_user:cgc_password@localhost:5432/cgc_db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # LLM
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4-turbo-preview"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"
    
    ANTHROPIC_API_KEY: Optional[str] = None
    ANTHROPIC_MODEL: str = "claude-3-opus-20240229"
    
    AZURE_OPENAI_API_KEY: Optional[str] = None
    AZURE_OPENAI_ENDPOINT: Optional[str] = None
    AZURE_OPENAI_MODEL: Optional[str] = None
    
    # Vector DB
    PGVECTOR_ENABLED: bool = True
    VECTOR_DIMENSION: int = 1536
    
    # Auth
    JWT_SECRET: str = "jwt-secret-key"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    
    # File Storage
    STORAGE_TYPE: str = "local"  # local, s3
    STORAGE_PATH: str = "./uploads"
    
    # AWS S3 (optional)
    AWS_S3_BUCKET: Optional[str] = None
    AWS_S3_REGION: str = "us-east-1"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Copilot
    COPILOT_MAX_TURNS: int = 10
    COPILOT_TEMPERATURE: float = 0.3
    COPILOT_MAX_TOKENS: int = 2000
    COPILOT_TOP_K: int = 5
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
