# database.py
import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config import settings

# Налаштування логування
logger = logging.getLogger(__name__)

# Створення асинхронного двигуна з використанням AFDATABASE_URL
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
)

# Фабрика асинхронних сесій
AsyncSessionFactory = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db():
    """Ініціалізація бази даних"""
    from models.base import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database initialized")

async def reset_db():
    """Скидання та створення нової бази даних"""
    from models.base import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database reset successfully")

async def close_db():
    """Закриття підключення до бази даних."""
    try:
        await engine.dispose()
        logger.info("Підключення до бази даних закрито")
    except Exception as e:
        logger.error(f"Помилка при закритті бази даних: {e}", exc_info=True)
