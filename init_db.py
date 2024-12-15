# init_db.py

import asyncio
import logging
from utils.db import engine
from models.base import Base
import models.user  # Імпортуємо модель User
import models.user_stats  # Імпортуємо модель UserStats

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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