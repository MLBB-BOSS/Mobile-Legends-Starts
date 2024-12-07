# config.py
import logging
from pydantic_settings import BaseSettings
import sys

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("ConfigLogger")


class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str
    OPENAI_API_KEY: str
    DATABASE_URL: str | None = None
    APP_NAME: str = "Mobile Legends Tournament Bot"
    DEBUG: bool = False

    @property
    def db_url(self) -> str | None:
        """
        Повертає відформатований URL для бази даних, якщо він заданий.
        """
        if not self.DATABASE_URL:
            logger.warning("DATABASE_URL не встановлено!")
            return None
        url = self.DATABASE_URL
        # Форматування для використання з asyncpg
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+asyncpg://", 1)
        logger.info("URL бази даних відформатовано успішно.")
        return url

    def validate(self):
        """
        Перевіряє необхідні налаштування.
        """
        if not self.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN не встановлено!")
        if not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY не встановлено!")
        if self.DEBUG:
            logger.info("Додаток працює в режимі DEBUG.")

    class Config:
        # env_file = ".env"  # Вилучено, оскільки ви використовуєте GitHub для деплою
        env_file_encoding = "utf-8"
        case_sensitive = True


# Створення екземпляра налаштувань
try:
    settings = Settings()
    # Валідація налаштувань
    settings.validate()
except Exception as e:
    logger.error(f"Помилка конфігурації: {e}")
    sys.exit(1)  # Завершити програму, якщо конфігурація некоректна
