# config.py
import logging
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str
    AS_BASE: str | None = None
    APP_NAME: str = "Mobile Legends Tournament Bot"
    DEBUG: bool = False

    @property
    def db_url(self) -> str | None:
        if not self.AS_BASE:
            logger.warning("AS_BASE is not set!")
            return None
        url = self.AS_BASE
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+asyncpg://", 1)
        logger.info("Database URL formatted successfully")
        return url

    def validate(self):
        if not self.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN is not set!")
        if self.DEBUG:
            logger.info("Application is running in DEBUG mode")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()

try:
    settings.validate()
except Exception as e:
    logger.error(f"Configuration error: {e}")
    raise