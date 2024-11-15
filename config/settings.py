from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional

class Settings(BaseSettings):
    # Bot configuration
    TELEGRAM_BOT_TOKEN: str = Field(
        ..., 
        env="TELEGRAM_BOT_TOKEN",
        description="Telegram Bot Token from @BotFather"
    )
    
    # Database configuration
    DATABASE_URL: Optional[str] = Field(
        None, 
        env="DATABASE_URL",
        description="Database connection URL"
    )
    ASYNC_DATABASE_URL: Optional[str] = Field(
        None, 
        env="ASYNC_DATABASE_URL",
        description="Async database connection URL"
    )
    
    # Throttling settings
    THROTTLE_RATE: float = Field(
        0.5, 
        env="THROTTLE_RATE",
        description="Rate limiting for bot commands"
    )
    
    # Development settings
    DEBUG: bool = Field(
        False, 
        env="DEBUG",
        description="Enable debug mode"
    )

    model_config = {
        "extra": "allow",
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True
    }

# Create settings instance
settings = Settings()
