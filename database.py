# UTC:23:14
# 2024-11-24
# database.py
# Author: MLBB-BOSS
# Description: Файл для роботи з базою даних
# The era of artificial intelligence.

import logging
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import async_sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from config import settings
from models.base import Base

# Налаштування логування
logger = logging.getLogger(__name__)

# Створення асинхронного двигуна бази даних
engine = create_async_engine(
    settings.DATABASE_URL, 
    echo=settings.DEBUG,
    pool_size=5,  # Розмір пулу з'єднань
    max_overflow=10  # Максимальна кількість додаткових з'єднань
)

# Створення сесії для роботи з базою даних
async_session = async_sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Функція для отримання сесії бази даних"""
    session = async_session()
    try:
        yield session
    except SQLAlchemyError as e:
        logger.error(f"Помилка бази даних: {str(e)}")
        await session.rollback()
        raise
    finally:
        await session.close()

async def init_db() -> None:
    """Функція для ініціалізації бази даних"""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Таблиці бази даних успішно створені")
    except SQLAlchemyError as e:
        logger.error(f"Помилка при створенні таблиць: {str(e)}")
        raise

async def close_db() -> None:
    """Функція для закриття з'єднань з базою даних"""
    try:
        await engine.dispose()
        logger.info("З'єднання з базою даних закриті")
    except SQLAlchemyError as e:
        logger.error(f"Помилка при закритті з'єднань: {str(e)}")
        raise
