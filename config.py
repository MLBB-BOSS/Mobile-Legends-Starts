from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str = Field(..., env='TELEGRAM_BOT_TOKEN')
    DATABASE_URL: str = Field(..., env='DATABASE_URL')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()
