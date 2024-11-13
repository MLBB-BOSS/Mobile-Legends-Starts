import os
from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import Optional

class Settings(BaseSettings):
    # Базові налаштування бота
    TELEGRAM_BOT_TOKEN: str
    
    # Налаштування бази даних
    DATABASE_URL: str
    
    # Налаштування логування
    LOG_LEVEL: str = "INFO"
    
    # Налаштування для збереження файлів
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 20 * 1024 * 1024  # 20MB в байтах
    
    @field_validator("DATABASE_URL")
    def validate_database_url(cls, v: Optional[str]) -> str:
        """
        Перевіряє і модифікує URL бази даних для правильної роботи з SQLAlchemy
        """
        if not v:
            raise ValueError("DATABASE_URL must be set")
        
        # Якщо використовується Heroku, замінюємо postgres:// на postgresql://
        if v.startswith("postgres://"):
            v = v.replace("postgres://", "postgresql://", 1)
        
        return v
    
    @field_validator("TELEGRAM_BOT_TOKEN")
    def validate_token(cls, v: Optional[str]) -> str:
        """
        Перевіряє наявність токену бота
        """
        if not v:
            raise ValueError("TELEGRAM_BOT_TOKEN must be set")
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

# Створюємо глобальний екземпляр налаштувань
settings = Settings()

# Створюємо директорію для завантажень, якщо вона не існує
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
