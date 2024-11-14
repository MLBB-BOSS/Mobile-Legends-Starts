# config/settings.py

from pydantic_settings import BaseSettings  # Імпортуємо BaseSettings з pydantic_settings
from pydantic import Field  # Імпортуємо Field з pydantic

class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str = Field(..., env="TELEGRAM_BOT_TOKEN")
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    ASYNC_DATABASE_URL: str = Field("", env="ASYNC_DATABASE_URL")

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
