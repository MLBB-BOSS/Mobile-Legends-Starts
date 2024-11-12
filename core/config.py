import os
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    DEBUG: bool = Field(default=False, env='DEBUG')
    DATABASE_URL: str = Field(..., env='DATABASE_URL')

    class Config:
        env_file = ".env"

settings = Settings()
