import os
import logging
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Завантаження .env файлу
load_dotenv()

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN")
    AS_BASE: str = os.getenv("AS_BASE")
    APP_NAME: str = "Mobile Legends Tournament Bot"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1")

    @property
    def db_url(self) -> str:
        """Повертає URL бази даних, відформатований для asyncpg."""
        if not self.AS_BASE:
            raise ValueError("AS_BASE is not set!")
        url = self.AS_BASE
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+asyncpg://", 1)
        logger.info(f"Database URL formatted: {url}")
        return url

    def validate(self):
        """Перевіряє обов'язкові змінні середовища."""
        if not self.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN is not set!")
        if not self.AS_BASE:
            raise ValueError("AS_BASE is not set!")
        logger.info("Configuration validated successfully.")

settings = Settings()

try:
    settings.validate()
except Exception as e:
    logger.error(f"Configuration error: {e}")
    raise