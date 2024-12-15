Ю# init_db.py

import asyncio
import logging
from config import engine, settings
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Імпорт моделей
import models.user  # Модель User
import models.user_stats  # Модель UserStats

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ініціалізація бази
Base = declarative_base()

async def init_db():
    logger.info("Initializing the database...")
    async with engine.begin() as conn:
        # Створення всіх таблиць
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database initialized successfully.")

if __name__ == "__main__":
    try:
        asyncio.run(init_db())
    except Exception as e:
        logger.error(f"Error initializing the database: {e}")
        raise
