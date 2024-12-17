import logging
from pydantic_settings import BaseSettings  # Новий імпорт для Pydantic 2.x
from pydantic import Field

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str = Field(..., env="TELEGRAM_BOT_TOKEN")
    DATABASE_URL: str = Field(..., env="DATABASE_URL")  # Стандартне підключення
    AS_BASE: str = Field(..., env="AS_BASE")  # Асинхронне підключення
    APP_NAME: str = Field("Mobile Legends: Starts (MLS)", env="APP_NAME")
    DEBUG: bool = Field(False, env="DEBUG")

    @property
    def db_url(self) -> str:
        """Повертає URL для асинхронного підключення."""
        url = self.AS_BASE or self.DATABASE_URL
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+asyncpg://", 1)
        logger.info("Database URL formatted successfully")
        return url

    def validate(self):
        """Перевіряє наявність необхідних налаштувань"""
        if not self.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN is not set!")
        if not (self.AS_BASE or self.DATABASE_URL):
            raise ValueError("No database URL is set!")
        if self.DEBUG:
            logger.info(f"{self.APP_NAME} is running in DEBUG mode")

    class Config:
        case_sensitive = True
        env_file = ".env"  # Додано підтримку .env файлу

# Створення екземпляру налаштувань
try:
    settings = Settings()
    settings.validate()
except Exception as e:
    logger.error(f"Configuration error: {e}")
    raise
