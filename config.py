# UTC:23:40
# 2024-11-24
# config.py
# Author: MLBB-BOSS
# Description: Конфігураційний файл з налаштуваннями бота
# The era of artificial intelligence.

import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Telegram Bot settings
    BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN")  # Змінено для сумісності
    
    # Database settings
    DATABASE_URL: str
    
    # Application settings
    APP_NAME: str = "Mobile Legends Tournament Bot"
    DEBUG: bool = False
    
    @property
    def db_url(self) -> str:
        """Повертає коректний URL для бази даних"""
        url = self.AFDATABASE_URL
        if url and url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+asyncpg://", 1)
        return url
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Створення єдиного екземпляру налаштувань
settings = Settings()
