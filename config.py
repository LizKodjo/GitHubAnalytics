import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import field_validator

class Settings(BaseSettings):
    """Application settings with validation"""
    
    # Flask
    SECRET_KEY: str = os.getenv("SECRET_KEY", "SECRET_KEY")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # GitHub API
    GITHUB_BASE_URL: str = "https://api.github.com"
    GITHUB_TOKEN: Optional[str] = os.getenv("GITHUB_TOKEN")
    
    # Redis for caching and rate limiting
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Security
    CORS_ORIGINS: list = ["http://localhost:3000", "http://127.0.0.1:3000"]
    RATE_LIMIT_PER_HOUR: int = 100
    
    # Sentry for error tracking
    SENTRY_DSN: Optional[str] = os.getenv("SENTRY_DSN")
    
    @field_validator("SECRET_KEY")
    def validate_secret_key(cls, v):
        if len(v) < 16:
            raise ValueError("SECRET_KEY must be at least 16 characters")
        return v

    class Config:
        env_file = ".env"

settings = Settings()