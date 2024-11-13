# config/settings.py

import os
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str = Field(..., env="TELEGRAM_BOT_TOKEN")
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    ASYNC_DATABASE_URL: str = Field("", env="ASYNC_DATABASE_URL")

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
