from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    # Основні налаштування
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    
    # Налаштування бази даних
    database_url: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost/dbname")
    async_database_url: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost/dbname_async")

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = False

settings = Settings()
