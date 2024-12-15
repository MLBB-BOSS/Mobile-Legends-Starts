# config.py

import logging
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Завантаження .env файлу
load_dotenv()

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str
    AS_BASE: str | None = None
    APP_NAME: str = "Mobile Legends Tournament Bot"
    DEBUG: bool = False

    @property
    def db_url(self) -> str:
        """Повертає відформатований URL бази даних."""
        if not self.AS_BASE:
            logger.warning("AS_BASE is not set!")
            raise ValueError("AS_BASE is не встановлений!")
        url = self.AS_BASE
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+asyncpg://", 1)
            logger.info("Замінено префікс PostgreSQL URL на asyncpg")
        return url

    def validate(self):
        """Перевіряє наявність необхідних налаштувань"""
        if not self.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN is не встановлений!")
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

# Створення асинхронного двигуна бази даних
engine = create_async_engine(settings.db_url, echo=settings.DEBUG)

# Створення асинхронної сесії
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

# Створення базового класу для моделей
Base = declarative_base()