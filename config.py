from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str = Field(..., env='TELEGRAM_BOT_TOKEN')
    DATABASE_URL: str = Field(..., env='DATABASE_URL')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

    @property
    def async_database_url(self):
        url = self.DATABASE_URL
        if url.startswith('postgres://'):
            # Replace 'postgres://' with 'postgresql+asyncpg://'
            url = url.replace('postgres://', 'postgresql+asyncpg://', 1)
        elif url.startswith('postgresql://'):
            # Add '+asyncpg' if it's not already present
            if '+asyncpg' not in url:
                url = url.replace('postgresql://', 'postgresql+asyncpg://', 1)
        return url

settings = Settings()
