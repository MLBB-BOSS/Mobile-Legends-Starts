from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # Основні налаштування бота
    TELEGRAM_BOT_TOKEN: str = Field(
        ..., 
        env="TELEGRAM_BOT_TOKEN",
        description="Telegram Bot Token from @BotFather"
    )
    
    # Налаштування для обмеження частоти запитів
    THROTTLE_RATE: float = Field(
        0.5, 
        env="THROTTLE_RATE",
        description="Rate limiting for bot commands"
    )
    
    # Режим розробки
    DEBUG: bool = Field(
        False, 
        env="DEBUG",
        description="Enable debug mode"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

# Create settings instance
settings = Settings()
