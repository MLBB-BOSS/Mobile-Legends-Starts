# database.py
# Created: 2024-11-24
# Author: MLBB-BOSS
# Description: Файл для роботи з базою даних

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config import settings

# Створення асинхронного двигуна бази даних
engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG)

# Створення сесії для роботи з базою даних
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_session() -> AsyncSession:
    """Функція для отримання сесії бази даних"""
    async with async_session() as session:
        yield session

async def create_tables():
    """Функція для створення всіх таблиць в базі даних"""
    from models.base import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
