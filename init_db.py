import asyncio
import logging
from utils.db import engine
from models.base import Base
import models.user  # Імпортуємо модель User
import models.user_stats  # Імпортуємо модель UserStats
import models.badge  # Імпортуємо модель Badge
import models.profile  # Імпортуємо модель Profile

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def init_db():
    """
    Функція для ініціалізації бази даних, створює всі таблиці, якщо їх ще немає.
    """
    logger.info("Initializing the database...")
    try:
        async with engine.begin() as conn:
            # Створення всіх таблиць
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing the database: {e}")
        raise

if __name__ == "__main__":
    try:
        asyncio.run(init_db())
    except Exception as e:
        logger.error(f"Critical error during database initialization: {e}")
        raise
