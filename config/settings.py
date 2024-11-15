from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Основні налаштування
    TELEGRAM_BOT_TOKEN: str
    
    # Налаштування бази даних
    database_url: str = "postgresql+asyncpg://user:password@localhost/dbname"
    async_database_url: str = "postgresql+asyncpg://user:password@localhost/dbname_async"

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = False  # Дозволяє використовувати різні стилі іменування змінних

settings = Settings()
