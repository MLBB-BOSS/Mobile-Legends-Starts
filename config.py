import logging
from pydantic_settings import BaseSettings
from pydantic import Field

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str = Field(..., env="TELEGRAM_BOT_TOKEN")
    AS_BASE: str = Field(..., env="AS_BASE")  # URL для асинхронного підключення (SQLAlchemy + aiomysql)
    DATABASE_URL: str = Field(..., env="DATABASE_URL")  # URL для синхронного підключення (SQLAlchemy + pymysql)
    APP_NAME: str = "mlbb"
    DEBUG: bool = False

    @property
    def db_sync_url(self) -> str:
        """Повертає URL для синхронного підключення (SQLAlchemy)."""
        url = self.DATABASE_URL
        logger.info("Sync Database URL retrieved successfully")
        return url

    @property
    def db_async_url(self) -> str:
        """Повертає URL для асинхронного підключення (SQLAlchemy + aiomysql)."""
        url = self.AS_BASE
        if url.startswith("mysql+aiomysql://"):
            logger.info("Async Database URL formatted correctly")
        else:
            logger.warning("Async Database URL does not start with 'mysql+aiomysql://'")
        return url

    def validate(self):
        """Перевіряє наявність необхідних налаштувань"""
        if not self.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN is not set!")
        if not self.AS_BASE or not self.DATABASE_URL:
            raise ValueError("Both AS_BASE and DATABASE_URL must be set!")
        if self.DEBUG:
            logger.info("Application is running in DEBUG mode")

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"

# Створення екземпляру налаштувань
settings = Settings()

# Валідація налаштувань
try:
    settings.validate()
except Exception as e:
    logger.error(f"Configuration error: {e}")
    raise