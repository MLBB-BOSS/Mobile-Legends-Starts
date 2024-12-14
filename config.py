import os
import logging
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str
    AS_BASE: str | None = None
    APP_NAME: str = "Mobile Legends Tournament Bot"
    DEBUG: bool = False

    @property
    def db_url(self) -> str | None:
        """Returns formatted database URL if it exists."""
        if not self.DATABASE_URL:
            logger.warning("DATABASE_URL is not set!")
            return None
        url = self.DATABASE_URL
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+asyncpg://", 1)
        logger.info("Database URL formatted successfully")
        return url

    def validate(self):
        """Validates required settings"""
        if not self.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN is not set!")
        if self.DEBUG:
            logger.info("Application is running in DEBUG mode")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

# Create settings instance
settings = Settings()

# Validate settings
try:
    settings.validate()
except Exception as e:
    logger.error(f"Configuration error: {e}")
    raise
