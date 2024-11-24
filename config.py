# config.py
# Created: 2024-11-24

from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    # Отримуємо токен напряму з змінних середовища
    TELEGRAM_BOT_TOKEN: str = os.getenv('TELEGRAM_BOT_TOKEN', '')
    
    # Отримуємо URL бази даних з змінних середовища 
    DATABASE_URL: str = os.getenv('DATABASE_URL', '')

    @property
    def async_database_url(self) -> str:
        # Конвертуємо URL для asyncpg
        if self.DATABASE_URL.startswith('postgres://'):
            return self.DATABASE_URL.replace('postgres://', 'postgresql+asyncpg://', 1)
        elif self.DATABASE_URL.startswith('postgresql://'):
            return self.DATABASE_URL.replace('postgresql://', 'postgresql+asyncpg://', 1)
        return self.DATABASE_URL

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

# Створюємо екземпляр налаштувань
settings = Settings()
