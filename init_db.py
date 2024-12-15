import asyncio
import logging
from utils.db import engine
from models.base import Base
import models.user  # Імпортуємо модель User
import models.user_stats  # Імпортуємо модель UserStats

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("init_db")

async def init_db():
    """Ініціалізація бази даних: створення таблиць."""
    try:
        logger.info("Starting database initialization...")
        async with engine.begin() as conn:
            # Видаляємо існуючі таблиці (опціонально)
            # await conn.run_sync(Base.metadata.drop_all)

            # Створюємо нові таблиці
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Error during database initialization: {e}")
        raise

if __name__ == "__main__":
    try:
        asyncio.run(init_db())
    except Exception as e:
        logger.critical(f"Critical error initializing the database: {e}")
        raise