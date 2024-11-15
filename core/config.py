from pydantic_settings import BaseSettings
from pydantic import PostgresDsn
import os
from datetime import datetime

class Settings(BaseSettings):
    # Базові налаштування бота
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    
    # Налаштування бази даних
    ASYNC_DATABASE_URL: PostgresDsn = os.getenv(
        "ASYNC_DATABASE_URL",
        "postgresql+asyncpg://u19gdelo8pjkrg:pb95edc1e9dc17f2d21f8f49fe9e9c6a3c2eab4969e95adbfc2c69a5c753b9fdb@ccaml3dimis7eh.cluster-czz5s0kz4scl.eu-west-1.rds.amazonaws.com:5432/da4c4gk6ldknbt"
    )
    
    # Налаштування середовища
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = ENVIRONMENT == "development"
    
    # Налаштування для обмеження запитів (rate limiting)
    RATE_LIMIT: int = 1  # секунди між повідомленнями
    
    # Налаштування логування
    LOG_LEVEL: str = "INFO"
    
    # Інформація про версію та час запуску
    VERSION: str = "1.0.0"
    START_TIME: datetime = datetime.utcnow()
    
    # Налаштування для кешування
    REDIS_URL: str = os.getenv("REDIS_URL", "")
    CACHE_TTL: int = 3600  # час життя кешу в секундах
    
    # Налаштування для адміністраторів
    ADMIN_IDS: list[int] = [
        # Додайте сюди ID адміністраторів
    ]
    
    # Налаштування гри
    MIN_NICKNAME_LENGTH: int = 3
    MAX_NICKNAME_LENGTH: int = 32
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"
    
    @property
    def uptime(self) -> float:
        return (datetime.utcnow() - self.START_TIME).total_seconds()

# Створюємо глобальний екземпляр налаштувань
settings = Settings()
