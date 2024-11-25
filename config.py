# UTC:23:40
# 2024-11-24
# config.py
# Author: MLBB-BOSS
# Description: Конфігураційний файл з налаштуваннями бота
# The era of artificial intelligence.

import os
import logging
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    # Telegram Bot settings
    BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN")
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    
    # Application settings
    APP_NAME: str = "Mobile Legends Tournament Bot"
    DEBUG: bool = False
    
    @property
    def db_url(self) -> str:
        """Повертає коректний URL для бази даних"""
        if not self.DATABASE_URL:
            logger.error("DATABASE_URL is not set!")
            raise ValueError("DATABASE_URL is not set!")
            
        url = self.DATABASE_URL
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+asyncpg://", 1)
        logger.info(f"Database URL formatted successfully (starts with: {url[:15]}...)")
        return url
    
    def validate(self):
        if not self.BOT_TOKEN:
            logger.error("TELEGRAM_BOT_TOKEN is not set!")
            raise ValueError("TELEGRAM_BOT_TOKEN is not set!")
        if not self.DATABASE_URL:
            logger.error("DATABASE_URL is not set!")
            raise ValueError("DATABASE_URL is not set!")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Створення єдиного екземпляру налаштувань
settings = Settings()
try:
    settings.validate()
except Exception as e:
    logger.error(f"Configuration error: {e}")
    raise
