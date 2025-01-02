from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import logging

# utils/db.py
from sqlalchemy.ext.declarative import declarative_base

# Імпортуємо ваші моделі
from utils.models import User, Item

Base = declarative_base()
# Не імпортуйте моделі тут, щоб уникнути циклічних імпортів

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@hostname/dbname")

async_engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Виводити SQL-запити в логи
    future=True
)

async_session = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("База даних ініціалізована успішно.")
