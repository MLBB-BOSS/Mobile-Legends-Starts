# config/settings.py

import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    ASYNC_DATABASE_URL: str = os.getenv("ASYNC_DATABASE_URL", "")

    class Config:
        env_file = ".env"

settings = Settings()
