"""
Core configuration settings for the AgriWaste2Fuel application
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
import os
from pathlib import Path

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """
    
    # Project Information
    PROJECT_NAME: str = "AgriWaste2Fuel"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "AI-powered platform for agricultural waste management"
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "sqlite:///./agri_waste.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # File Upload
    MAX_FILE_SIZE: int = 10485760  # 10MB
    ALLOWED_IMAGE_TYPES: List[str] = [
        "image/jpeg", 
        "image/png", 
        "image/jpg", 
        "image/gif"
    ]
    
    # Mock Settings (for development)
    MOCK_MODE: bool = True
    ML_MODEL_ENABLED: bool = False
    
    # Carbon Credit Market Rate (INR per credit)
    CARBON_CREDIT_RATE: float = 1500.0
    
    # Directories
    UPLOAD_DIR: str = "uploads"
    CERTIFICATES_DIR: str = "certificates"
    
    # Firebase Configuration
    ENVIRONMENT: str = "development"
    FIREBASE_SERVICE_ACCOUNT_KEY: str = ""
    FIREBASE_CONFIG: str = ""
    
    class Config:
        env_file = ".env"
        extra = "allow"  # Allow extra fields from .env file
        case_sensitive = True

# Create settings instance
settings = Settings()

# Ensure directories exist
Path(settings.UPLOAD_DIR).mkdir(exist_ok=True)
Path(settings.CERTIFICATES_DIR).mkdir(exist_ok=True)
