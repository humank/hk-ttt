"""
Application configuration settings.
"""

import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Opportunity Management Service API"
    VERSION: str = "1.0.0"
    
    # Database Settings
    DATABASE_URL: str = "sqlite:///./opportunity_management.db"
    
    # CORS Settings
    ALLOWED_HOSTS: List[str] = ["*"]  # For development - restrict in production
    
    # File Upload Settings
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE: int = 20 * 1024 * 1024  # 20MB
    ALLOWED_FILE_TYPES: List[str] = ["*"]  # All file types allowed
    
    # Rate Limiting Settings
    RATE_LIMIT_PER_MINUTE: int = 100
    RATE_LIMIT_PER_HOUR: int = 1000
    
    # Logging Settings
    LOG_LEVEL: str = "INFO"
    
    # Pagination Settings
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()
