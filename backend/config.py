import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Recruitment Intelligence Engine"
    app_version: str = "1.0.0"
    environment: str = "development"
    log_level: str = "INFO"
    
    # Anthropic API Key
    anthropic_api_key: str = ""
    claude_model: str = "claude-opus-4-1-20250805"
    
    # Database
    database_url: str = "sqlite:///./recruiter.db"
    
    # File limits
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    max_resumes_per_batch: int = 50
    upload_dir: str = "./uploads"
    
    # CORS
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
    ]

settings = Settings()

# Ensure upload directory exists
os.makedirs(settings.upload_dir, exist_ok=True)
