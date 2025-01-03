# utils/db.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import logging
import os

# Імпорт базового класу з окремого модуля
from utils.base import Base
from utils.models import User, Item  # Локальний імпорт для уникнення циклічних залежностей

from utils.settings import settings  # Імпорт налаштувань

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Використання ASYNC_DATABASE_URL з налаштувань
DATABASE_URL = settings.ASYNC_DATABASE_URL or "postgresql+asyncpg://user:password@hostname/dbname"

# Створення асинхронного двигуна бази даних
async_engine = create_async_engine(
    DATABASE_URL,
    echo=settings.DEBUG,  # Виводити SQL-запити в логи, якщо DEBUG=True
    future=True
)

# Створення фабрики сесій
async_session = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db():
    """
    Ініціалізація бази даних.
    Створює всі таблиці, визначені моделями.
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("База даних ініціалізована успішно.")
