from pydantic_settings import BaseSettings
from pydantic import SecretStr, ValidationError
import os


class Config(BaseSettings):
    # Основні налаштування
    TELEGRAM_BOT_TOKEN: SecretStr

    class Config:
        env_file = ".env"  # Вмикаємо підтримку файлу .env для локального тестування
        case_sensitive = True  # Змінні чутливі до регістру


# Функція для створення екземпляра конфігурації
def load_config() -> Config:
    try:
        return Config()  # Завантажуємо налаштування з середовища або .env
    except ValidationError as e:
        print("Помилка валідації конфігурації:")
        print(e)
        raise ValueError("Перевірте налаштування змінних середовища або .env файл.")


# Створюємо екземпляр конфігурації
config = load_config()


# Валідація при імпорті
def validate_config() -> None:
    if not config.TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN не налаштовано в змінних середовища або .env файлі")


validate_config()
