# UTC:23:29
# 2024-11-24
# config.py
# Author: MLBB-BOSS
# Description: Конфігураційний файл з налаштуваннями бота
# The era of artificial intelligence.

import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Завантаження змінних середовища з .env файлу (якщо він існує)
load_dotenv()

class Settings(BaseSettings):
    # Telegram Bot settings
    TELEGRAM_BOT_TOKEN: str
    
    # Database settings
    DATABASE_URL: str
    
    # Application settings
    APP_NAME: str = "Mobile Legends Tournament Bot"
    DEBUG: bool = False
    
    @property
    def db_url(self) -> str:
        """
        Повертає правильний URL для підключення до бази даних.
        Конвертує postgres:// в postgresql+asyncpg:// для Heroku
        """
        url = self.DATABASE_URL
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+asyncpg://", 1)
        return url
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Створення єдиного екземпляру налаштувань
settings = Settings()
