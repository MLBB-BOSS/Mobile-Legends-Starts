# utils/settings.py
from pydantic_settings import BaseSettings
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    # База даних
    DATABASE_URL: str = "postgres://ufk3frgco7l9d1:p7aad477be5e7c084f8d9c2e9998fdfd75ed3eb573c808a6b3db95bbdb221b234@ccaml3dimis7eh.cluster-czz5s0kz4scl.eu-west-1.rds.amazonaws.com:5432/d7rglea9jc6ggd"
    ASYNC_DATABASE_URL: Optional[str] = None
    
    # Telegram
    TELEGRAM_BOT_TOKEN: str
    
    # Налаштування додатку
    DEBUG: bool = False
    APP_NAME: str = "MLBB Tournament Bot"
    
    # Налаштування пулу з'єднань
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Конвертуємо URL для асинхронного з'єднання
        if self.DATABASE_URL and not self.ASYNC_DATABASE_URL:
            self.ASYNC_DATABASE_URL = self.DATABASE_URL.replace(
                'postgres://', 'postgresql+asyncpg://'
            )
            # Для синхронного з'єднання
            self.DATABASE_URL = self.DATABASE_URL.replace(
                'postgres://', 'postgresql://'
            )

settings = Settings()
