# File: config/settings.py
from pydantic_settings import BaseSettings
from pydantic import SecretStr
import os

class Config(BaseSettings):
    # Основні налаштування
    TELEGRAM_BOT_TOKEN: SecretStr = os.environ["TELEGRAM_BOT_TOKEN"]
    
    class Config:
        env_file = None  # Відключаємо завантаження з .env файлу
        case_sensitive = True

# Створюємо екземпляр конфігурації
config = Config()

# Валідація при імпорті
def validate_config() -> None:
    if not config.TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN не налаштовано в змінних середовища Heroku")

validate_config()
