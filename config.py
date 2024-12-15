# config.py

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
    AS_BASE: str | None = None
    APP_NAME: str = "Mobile Legends Tournament Bot"
    DEBUG: bool = False

    @property
    def db_url(self) -> str | None:
        """Повертає відформатований URL бази даних, якщо він існує."""
        if not self.AS_BASE:
            logger.warning("AS_BASE is not set!")
            return None
        url = self.AS_BASE
        if url.startswith("postgres://"):
            url = url.replace("postgresql+asyncpg://ufk3frgco7l9d1:p7aad477be5e7c084f8d9c2e9998fdfd75ed3eb573c808a6b3db95bbdb221b234@ccaml3dimis7eh.cluster-czz5s0kz4scl.eu-west-1.rds.amazonaws.com:5432/d7rglea9jc6ggd")

if not AS_BASE:
    raise ValueError("AS_BASE is not set or invalid")

engine = create_async_engine(AS_BASE, echo=False)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)", 1)
        logger.info("Database URL formatted successfully")
        return url

    def validate(self):
        """Перевіряє наявність необхідних налаштувань"""
        if not self.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN is not set!")
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
