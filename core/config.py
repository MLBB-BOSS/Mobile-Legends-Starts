from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, Field
import os
from datetime import datetime
from typing import List

class Settings(BaseSettings):
    # Базові налаштування бота
    TELEGRAM_BOT_TOKEN: str = Field(..., env='TELEGRAM_BOT_TOKEN')
    
    # Налаштування бази даних
    ASYNC_DATABASE_URL: PostgresDsn = Field(
        default="postgresql+asyncpg://u19gdelo8pjkrg:pb95edc1e9dc17f2d21f8f49fe9e9c6a3c2eab4969e95adbfc2c69a5c753b9fdb@ccaml3dimis7eh.cluster-czz5s0kz4scl.eu-west-1.rds.amazonaws.com:5432/da4c4gk6ldknbt"
    )
    
    # Резервні налаштування бази даних
    POSTGRES_USER: str = Field(default="u19gdelo8pjkrg")
    POSTGRES_PASSWORD: str = Field(default="pb95edc1e9dc17f2d21f8f49fe9e9c6a3c2eab4969e95adbfc2c69a5c753b9fdb")
    POSTGRES_HOST: str = Field(default="ccaml3dimis7eh.cluster-czz5s0kz4scl.eu-west-1.rds.amazonaws.com")
    POSTGRES_PORT: str = Field(default="5432")
    POSTGRES_DB: str = Field(default="da4c4gk6ldknbt")
    
    # Налаштування середовища
    ENVIRONMENT: str = Field(default="development")
    DEBUG: bool = Field(default=False)
    
    # Налаштування пулу підключень
    DB_ECHO: bool = Field(default=False)
    DB_POOL_SIZE: int = Field(default=5)
    DB_MAX_OVERFLOW: int = Field(default=10)
    DB_POOL_TIMEOUT: int = Field(default=30)
    
    # Налаштування для обмеження запитів
    RATE_LIMIT: float = Field(default=0.5)
    
    # Налаштування логування
    LOG_LEVEL: str = Field(default="INFO")
    
    # Інформація про версію та час запуску
    VERSION: str = "1.0.0"
    START_TIME: datetime = Field(default_factory=datetime.utcnow)
    
    # Налаштування для кешування
    REDIS_URL: str = Field(default="")
    CACHE_TTL: int = Field(default=3600)
    
    # Налаштування для адміністраторів
    ADMIN_IDS: List[int] = Field(default_factory=list)
    
    # Налаштування гри
    MIN_NICKNAME_LENGTH: int = Field(default=3)
    MAX_NICKNAME_LENGTH: int = Field(default=32)
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"
    
    @property
    def database_url(self) -> str:
        """
        Повертає URL бази даних, використовуючи ASYNC_DATABASE_URL або складає з окремих параметрів
        """
        if self.ASYNC_DATABASE_URL:
            return str(self.ASYNC_DATABASE_URL)
        
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    @property
    def uptime(self) -> float:
        return (datetime.utcnow() - self.START_TIME).total_seconds()

# Створюємо глобальний екземпляр налаштувань
settings = Settings()
