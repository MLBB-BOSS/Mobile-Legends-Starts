from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional

class Settings(BaseSettings):
    # Bot configuration
    TELEGRAM_BOT_TOKEN: str = Field(..., env="TELEGRAM_BOT_TOKEN", description="Telegram Bot Token from @BotFather")
    
    # Optional webhook settings (if you plan to use webhook instead of polling)
    WEBHOOK_HOST: Optional[str] = Field(None, env="WEBHOOK_HOST")
    WEBHOOK_PATH: Optional[str] = Field(None, env="WEBHOOK_PATH")
    WEBAPP_HOST: str = Field("0.0.0.0", env="WEBAPP_HOST")
    WEBAPP_PORT: int = Field(8000, env="WEBAPP_PORT")
    
    # Database configuration (if you plan to add database)
    DATABASE_URL: Optional[str] = Field(None, env="DATABASE_URL")
    
    # Redis configuration (if you plan to use Redis for FSM or rate limiting)
    REDIS_HOST: Optional[str] = Field(None, env="REDIS_HOST")
    REDIS_PORT: int = Field(6379, env="REDIS_PORT")
    REDIS_DB: int = Field(0, env="REDIS_DB")
    
    # Throttling settings
    THROTTLE_RATE: float = Field(0.5, env="THROTTLE_RATE")
    
    # Development settings
    DEBUG: bool = Field(False, env="DEBUG")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

    @property
    def webhook_url(self) -> Optional[str]:
        """Get webhook URL if webhook mode is enabled"""
        if self.WEBHOOK_HOST and self.WEBHOOK_PATH:
            return f"{self.WEBHOOK_HOST}{self.WEBHOOK_PATH}"
        return None

    @property
    def is_webhook_mode(self) -> bool:
        """Check if webhook mode is enabled"""
        return bool(self.webhook_url)

# Create settings instance
settings = Settings()
