from pydantic_settings import BaseSettings
import os
import logging

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    # Telegram Bot settings
    TELEGRAM_BOT_TOKEN: str

    # Database settings
    DATABASE_URL: str = os.getenv('DATABASE_URL', '')
    ASYNC_DATABASE_URL: str = ''
    DEBUG: bool = False

    def __init__(self, **data):
        super().__init__(**data)
        
        # Перетворення DATABASE_URL в ASYNC_DATABASE_URL
        if self.DATABASE_URL.startswith('postgres://'):
            self.DATABASE_URL = self.DATABASE_URL.replace('postgres://', 'postgresql://', 1)
            
        # Створення асинхронного URL
        if self.DATABASE_URL:
            self.ASYNC_DATABASE_URL = self.DATABASE_URL.replace('postgresql://', 'postgresql+asyncpg://', 1)
            logger.info("Async Database URL created successfully")
        else:
            logger.warning("Database URL is not set")

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()
