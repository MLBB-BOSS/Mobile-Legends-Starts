# utils/settings.py
from pydantic_settings import BaseSettings
import os
import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str
    DATABASE_URL: str | None = None
    ASYNC_DATABASE_URL: str | None = None
    DEBUG: bool = False

    def model_post_init(self, *args, **kwargs):
        database_url = os.getenv('DATABASE_URL')

        if database_url:
            # Конвертуємо URL в правильний формат
            if database_url.startswith('postgres://'):
                database_url = database_url.replace('postgres://', 'postgresql://', 1)

            self.DATABASE_URL = database_url
            self.ASYNC_DATABASE_URL = database_url.replace('postgresql://', 'postgresql+asyncpg://', 1)

            # Логуємо успішне налаштування (без конфіденційних даних)
            parsed_url = urlparse(self.DATABASE_URL)
            logger.info(f"Database configured: {parsed_url.hostname}")
        else:
            logger.error("DATABASE_URL not found in environment variables")
            raise ValueError("DATABASE_URL environment variable is required")

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = 'ignore'

settings = Settings()
