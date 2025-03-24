from typing import List, Union
from pydantic import BaseSettings, AnyHttpUrl, validator

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Lead Generation API"
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:5173"]
    
    # Security
    SECRET_KEY: str = "64f8b15de7cee880318e5feca119889cb282d25df15ba89ca3f194c5e01205af"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 11520  # 8 days
    
    # OpenAI
    OPENAI_API_KEY: str = "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"
    
    # LinkedIn
    LINKEDIN_USERNAME: str = "bobthebuilde444@gmail.com"
    LINKEDIN_PASSWORD: str = "bobthebuilder1@"
    
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