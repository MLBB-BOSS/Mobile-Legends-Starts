import asyncio
import logging
from utils.db import engine
from models.base import Base
import models.user  # Модель користувача
import models.badge  # Модель бейджів
import models.user_stats  # Модель статистики

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def init_db():
    """Створення всіх таблиць"""
    logger.info("Initializing the database...")
    async with engine.begin() as conn:
        # Перевірка та створення таблиць
        await conn.run_sync(Base.metadata.create_all, checkfirst=True)
    logger.info("Database initialized successfully.")

if __name__ == "__main__":
    try:
        asyncio.run(init_db())
    except Exception as e:
        logger.error(f"Error initializing the database: {e}")
        raise
