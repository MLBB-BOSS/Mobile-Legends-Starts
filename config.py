import logging
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Завантаження .env файлу
load_dotenv()

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str
    DATABASE_URL: str
    APP_NAME: str = "Mobile Legends Starts"
    DEBUG: bool = False

    @property
    def db_url(self) -> str:
        """Перевіряє та повертає URL бази даних."""
        url = self.DATABASE_URL
        if not url:
            logger.warning("DATABASE_URL is not set!")
            raise ValueError("DATABASE_URL is required but not set!")
        logger.info("Database URL loaded successfully")
        return url

    def validate(self):
        """Перевіряє наявність необхідних налаштувань"""
        if not self.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN is not set!")
        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL is not set!")
        if self.DEBUG:
            logger.info("Application is running in DEBUG mode")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

# Створення екземпляру налаштувань
settings = Settings()

# Валідація налаштувань
try:
    settings.validate()
except Exception as e:
    logger.error(f"Configuration error: {e}")
    raise
