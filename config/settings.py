from pathlib import Path
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
    UPLOAD_DIR: Path = Path("uploads")
    MAX_FILE_SIZE: int = 20 * 1024 * 1024  # 20MB в байтах
    
    @field_validator("DATABASE_URL")
    def validate_database_url(cls, v: str) -> str:
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
    def validate_token(cls, v: str) -> str:
        """
        Перевіряє наявність токену бота
        """
        if not v:
            raise ValueError("TELEGRAM_BOT_TOKEN must be set")
        return v
    
    @field_validator("UPLOAD_DIR")
    def validate_upload_dir(cls, v: Path) -> Path:
        """
        Перевіряє чи директорія для завантажень існує або створює її
        """
        if not v.exists():
            v.mkdir(parents=True, exist_ok=True)
        if not v.is_dir():
            raise ValueError("UPLOAD_DIR must be a directory")
        return v
    
    @field_validator("LOG_LEVEL")
    def validate_log_level(cls, v: str) -> str:
        """
        Перевіряє, чи рівень логування є допустимим
        """
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if v not in valid_levels:
            raise ValueError(f"LOG_LEVEL must be one of {valid_levels}")
        return v
    
    @field_validator("MAX_FILE_SIZE")
    def validate_max_file_size(cls, v: int) -> int:
        """
        Перевіряє, чи максимальний розмір файлу є позитивним числом
        """
        if v <= 0:
            raise ValueError("MAX_FILE_SIZE must be a positive integer")
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        env_prefix = "APP_"

# Створюємо глобальний екземпляр налаштувань
settings = Settings()

# Створюємо директорію для завантажень, якщо вона не існує
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
