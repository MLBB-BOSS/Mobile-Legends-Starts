from pydantic_settings import BaseSettings
import os
import logging
from typing import Optional
from urllib.parse import urlparse
from datetime import datetime

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    # Bot Info
    CURRENT_TIME: str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    CURRENT_USER: str = "MLBB-BOSS"
    
    # Telegram
    TELEGRAM_BOT_TOKEN: str = "7721474356:AAEYb4YIEAKCCxMl3uxT8t__KAiwQ4UopkQ"
    
    # Database
    DATABASE_URL: str = "postgres://ufk3frgco7l9d1:p7aad477be5e7c084f8d9c2e9998fdfd75ed3eb573c808a6b3db95bbdb221b234@ccaml3dimis7eh.cluster-czz5s0kz4scl.eu-west-1.rds.amazonaws.com:5432/d7rglea9jc6ggd"
    AS_BASE: str = "postgresql+asyncpg://ufk3frgco7l9d1:p7aad477be5e7c084f8d9c2e9998fdfd75ed3eb573c808a6b3db95bbdb221b234@ccaml3dimis7eh.cluster-czz5s0kz4scl.eu-west-1.rds.amazonaws.com:5432/d7rglea9jc6ggd"
    
    # Database settings
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    
    # Application
    DEBUG: bool = False
    APP_NAME: str = "MLBB Tournament Bot"
    VERSION: str = "1.0.0"

    def model_post_init(self, *args, **kwargs):
        logger.info(f"Initializing configuration for {self.APP_NAME}")
        logger.info(f"Current time: {self.CURRENT_TIME}")
        logger.info(f"Current user: {self.CURRENT_USER}")
        
        parsed_url = urlparse(self.AS_BASE)
        logger.info(f"Database configured: {parsed_url.scheme}://{parsed_url.hostname}")

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = True

# Create settings instance
settings = Settings()
