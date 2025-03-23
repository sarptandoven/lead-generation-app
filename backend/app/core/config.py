from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/leadgen")

    # LinkedIn
    LINKEDIN_USERNAME: str = os.getenv("LINKEDIN_USERNAME", "")
    LINKEDIN_PASSWORD: str = os.getenv("LINKEDIN_PASSWORD", "")

    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # Application
    APP_SECRET_KEY: str = os.getenv("APP_SECRET_KEY", "your-secret-key-here")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"

    # Rate Limiting
    MAX_REQUESTS_PER_MINUTE: int = int(os.getenv("MAX_REQUESTS_PER_MINUTE", "30"))
    MAX_REQUESTS_PER_HOUR: int = int(os.getenv("MAX_REQUESTS_PER_HOUR", "1000"))

    # Proxy Settings
    PROXY_LIST: Optional[str] = os.getenv("PROXY_LIST", None)

    # Email Verification
    EMAIL_VERIFICATION_API_KEY: Optional[str] = os.getenv("EMAIL_VERIFICATION_API_KEY", None)

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "app.log")

    class Config:
        case_sensitive = True

settings = Settings() 