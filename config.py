from pydantic_settings import BaseSettings
import os
import logging
from typing import Optional
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    # Основні налаштування
    TELEGRAM_BOT_TOKEN: str
    DATABASE_URL: Optional[str] = None
    ASYNC_DATABASE_URL: Optional[str] = None
    DEBUG: bool = False
    
    # Налаштування бази даних
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_ECHO: bool = False  # Для відображення SQL запитів
    
    # Налаштування застосунку
    APP_TITLE: str = "MLBB Tournament Bot"
    APP_VERSION: str = "1.0.0"
    
    def model_post_init(self, *args, **kwargs):
        database_url = os.getenv('DATABASE_URL')
        
        if database_url:
            # Конвертуємо URL для синхронного з'єднання
            if database_url.startswith('postgres://'):
                self.DATABASE_URL = database_url.replace('postgres://', 'postgresql://', 1)
            else:
                self.DATABASE_URL = database_url
                
            # Конвертуємо URL для асинхронного з'єднання
            self.ASYNC_DATABASE_URL = self.DATABASE_URL.replace(
                'postgresql://', 
                'postgresql+asyncpg://', 
                1
            )
            
            # Безпечне логування
            parsed_url = urlparse(self.DATABASE_URL)
            logger.info(f"Database configured: {parsed_url.scheme}://*****@{parsed_url.hostname}")
        else:
            logger.error("DATABASE_URL not found in environment variables")
            raise ValueError("DATABASE_URL environment variable is required")

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = 'ignore'

settings = Settings()
