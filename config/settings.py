# config/settings.py

from pydantic_settings import BaseSettings
from pydantic import Field
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str = Field(..., env="TELEGRAM_BOT_TOKEN")
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    ASYNC_DATABASE_URL: str = Field("", env="ASYNC_DATABASE_URL")
    DEBUG: bool = Field(False, env="DEBUG")

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

logger.debug("Settings loaded successfully")
