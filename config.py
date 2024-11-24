# config.py
# Created: 2024-11-24
# Author: MLBB-BOSS
# Description: Конфігураційний файл для налаштування бота та бази даних

from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    # Токен бота Telegram, отриманий від BotFather
    TELEGRAM_BOT_TOKEN: str = os.environ.get('TELEGRAM_BOT_TOKEN')
    
    # URL підключення до бази даних PostgreSQL
    DATABASE_URL: str = os.environ.get('DATABASE_URL')

    @property
    def async_database_url(self) -> str:
        """Конвертує стандартний URL бази даних в асинхронний формат для asyncpg"""
        if not self.DATABASE_URL:
            return ''
        
        if self.DATABASE_URL.startswith('postgres://'):
            return self.DATABASE_URL.replace('postgres://', 'postgresql+asyncpg://', 1)
        elif self.DATABASE_URL.startswith('postgresql://'):
            return self.DATABASE_URL.replace('postgresql://', 'postgresql+asyncpg://', 1)
        return self.DATABASE_URL

    class Config:
        case_sensitive = True
        env_file = '.env'
        env_file_encoding = 'utf-8'

# Створюємо екземпляр налаштувань
settings = Settings()

# Перевірка наявності критичних змінних
if not settings.TELEGRAM_BOT_TOKEN:
    raise ValueError("Не встановлено TELEGRAM_BOT_TOKEN")
