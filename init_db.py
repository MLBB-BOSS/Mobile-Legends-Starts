import asyncio
import logging
from utils.db import engine
from models.base import Base
import models.user  # Імпортуємо модель User
import models.user_stats  # Імпортуємо модель UserStats
import models.badge  # Імпортуємо модель Badge

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def init_db():
    """Ініціалізація бази даних"""
    logger.info("Initializing the database...")
    try:
        async with engine.begin() as conn:
            # Створення всіх таблиць, якщо вони ще не існують
            await conn.run_sync(Base.metadata.create_all, checkfirst=True)
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing the database: {e}")
        raise

if __name__ == "__main__":
    try:
        asyncio.run(init_db())
    except Exception as e:
        logger.error(f"Error initializing the database: {e}")
        raise
