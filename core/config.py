from pydantic_settings import BaseSettings
from pydantic import Field
import os
from dotenv import load_dotenv

# Завантажуємо змінні середовища з .env файлу
load_dotenv()

class Settings(BaseSettings):
    # Налаштування бота
    TELEGRAM_BOT_TOKEN: str = Field(..., env='BOT_TOKEN')
    ADMIN_IDS: list[int] = Field(default_factory=list)
    
    # Налаштування бази даних
    POSTGRES_USER: str = Field(env='POSTGRES_USER', default="")
    POSTGRES_PASSWORD: str = Field(env='POSTGRES_PASSWORD', default="")
    POSTGRES_HOST: str = Field(env='POSTGRES_HOST', default="")
    POSTGRES_PORT: str = Field(env='POSTGRES_PORT', default="5432")
    POSTGRES_DB: str = Field(env='POSTGRES_DB', default="")
    
    @property
    def DATABASE_URL(self) -> str:
        """Формуємо URL для підключення до бази даних"""
        # Перевіряємо, чи є змінна DATABASE_URL в env
        if os.getenv('DATABASE_URL'):
            return os.getenv('DATABASE_URL')
        
        # Якщо немає, формуємо з окремих компонентів
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    # Налаштування бази даних
    DB_ECHO: bool = Field(default=False, env='DB_ECHO')
    DB_POOL_SIZE: int = Field(default=5, env='DB_POOL_SIZE')
    DB_MAX_OVERFLOW: int = Field(default=10, env='DB_MAX_OVERFLOW')
    DB_POOL_TIMEOUT: int = Field(default=30, env='DB_POOL_TIMEOUT')
    
    # Налаштування логування
    LOG_LEVEL: str = Field(default='INFO', env='LOG_LEVEL')
    
    # Налаштування rate limiting
    RATE_LIMIT: float = Field(default=0.5, env='RATE_LIMIT')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

# Створюємо екземпляр налаштувань
settings = Settings()
