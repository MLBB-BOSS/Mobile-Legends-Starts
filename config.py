from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str
    DATABASE_URL: str = os.getenv('DATABASE_URL', '')

    @property
    def async_database_url(self) -> str:
        # Перевіряємо, чи це Heroku DATABASE_URL
        if self.DATABASE_URL.startswith('postgres://'):
            return self.DATABASE_URL.replace('postgres://', 'postgresql+asyncpg://', 1)
        elif self.DATABASE_URL.startswith('postgresql://'):
            return self.DATABASE_URL.replace('postgresql://', 'postgresql+asyncpg://', 1)
        return self.DATABASE_URL

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()
