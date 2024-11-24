# config.py
# Created: 2024-11-24
# Author: MLBB-BOSS
# Description: Конфігураційний файл з налаштуваннями бота

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Telegram Bot settings
    TELEGRAM_BOT_TOKEN: str
    
    # Database settings
    DATABASE_URL: str
    
    # Application settings
    APP_NAME: str = "MLS Bot"
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
