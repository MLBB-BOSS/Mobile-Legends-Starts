import os
import logging
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    # Ensure this matches exactly with your Heroku config var name
    TELEGRAM_BOT_TOKEN: str
    DATABASE_URL: str | None = None
    
    # Application settings
    APP_NAME: str = "Mobile Legends Tournament Bot"
    DEBUG: bool = False
    
    @property
    def db_url(self) -> str | None:
        """Returns formatted database URL if it exists"""
        if not self.DATABASE_URL:
            return None
            
        url = self.DATABASE_URL
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+asyncpg://", 1)
        logger.info(f"Database URL formatted successfully")
        return url
    
    def validate(self):
        """Validates required settings"""
        if not self.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN is not set!")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        # This ensures case-sensitive matching with env vars
        case_sensitive = True

# Create settings instance
settings = Settings()

# Validate settings
try:
    settings.validate()
except Exception as e:
    logger.error(f"Configuration error: {e}")
    raise
