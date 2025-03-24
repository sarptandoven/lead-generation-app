from typing import List, Union
from pydantic import BaseSettings, AnyHttpUrl, validator
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Lead Generation API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # LinkedIn credentials (optional)
    LINKEDIN_USERNAME: str = os.getenv("LINKEDIN_USERNAME", "")
    LINKEDIN_PASSWORD: str = os.getenv("LINKEDIN_PASSWORD", "")
    
    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "https://localhost",
        "https://localhost:8080",
        "*"  # Allow all origins in development
    ]
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Security
    SECRET_KEY: str = "64f8b15de7cee880318e5feca119889cb282d25df15ba89ca3f194c5e01205af"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 11520  # 8 days
    
    # Application Settings
    LOG_LEVEL: str = "INFO"
    MAX_WORKERS: int = 4
    MAX_RETRIES: int = 5
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 