from pydantic_settings import BaseSettings
import os
import logging

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    # Telegram Bot settings
    TELEGRAM_BOT_TOKEN: str

    # Database settings
    DATABASE_URL: str | None = None
    ASYNC_DATABASE_URL: str | None = None
    DEBUG: bool = False

    def model_post_init(self, *args, **kwargs):
        """Виконується після ініціалізації моделі"""
        # Отримуємо URL з змінної середовища Heroku
        database_url = os.getenv('DATABASE_URL')
        
        if database_url:
            # Конвертуємо URL для PostgreSQL
            if database_url.startswith('postgres://'):
                database_url = database_url.replace('postgres://', 'postgresql://', 1)
            
            self.DATABASE_URL = database_url
            self.ASYNC_DATABASE_URL = database_url.replace('postgresql://', 'postgresql+asyncpg://', 1)
            logger.info("Database URLs configured successfully")
        else:
            logger.warning("DATABASE_URL not found in environment variables")
            # Встановлюємо значення за замовчуванням або викидаємо помилку
            self.DATABASE_URL = "sqlite:///./test.db"
            self.ASYNC_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        # Дозволяємо використання додаткових змінних середовища
        extra = 'ignore'

# Створюємо екземпляр налаштувань
settings = Settings()
