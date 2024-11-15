from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # Bot settings
    TELEGRAM_BOT_TOKEN: str = Field(..., env='TELEGRAM_BOT_TOKEN')
    
    # Database settings
    ASYNC_DATABASE_URL: str = Field(..., env='ASYNC_DATABASE_URL')
    
    # Environment settings
    ENVIRONMENT: str = Field(default="development")
    DEBUG: bool = Field(default=False)
    
    # Rate limiting
    RATE_LIMIT: float = Field(default=0.5)
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
