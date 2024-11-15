# core/config.py
from pydantic_settings import BaseSettings
from pydantic import Field, PostgresDsn
from datetime import datetime

class Settings(BaseSettings):
    # Базові налаштування бота
    TELEGRAM_BOT_TOKEN: str = Field(..., env='TELEGRAM_BOT_TOKEN')
    
    # База даних
    DATABASE_URL: PostgresDsn = Field(..., env='DATABASE_URL')
    
    # Налаштування середовища
    ENVIRONMENT: str = Field(default="development")
    DEBUG: bool = Field(default=False)
    
    # Базові налаштування
    RATE_LIMIT: float = Field(default=0.5)
    LOG_LEVEL: str = Field(default="INFO")
    
    # Адміністратори
    ADMIN_IDS: list[int] = Field(default_factory=list)
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
