from pydantic_settings import BaseSettings
from pydantic import Field, PostgresDsn
from typing import Optional

class Settings(BaseSettings):
    # Bot configuration
    TELEGRAM_BOT_TOKEN: str = Field(
        ..., 
        env="TELEGRAM_BOT_TOKEN",
        description="Telegram Bot Token from @BotFather"
    )
    
    # Database configuration
    DATABASE_URL: Optional[PostgresDsn] = Field(
        None, 
        env="DATABASE_URL",
        description="Database connection URL"
    )
    ASYNC_DATABASE_URL: Optional[PostgresDsn] = Field(
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
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
        "extra": "ignore",  # Allow extra fields in the environment
        "validate_default": True,
        "protected_namespaces": ()
    }

# Create settings instance
settings = Settings()
