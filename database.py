# database.py
import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from aiogram import BaseMiddleware

from config import settings
from models.base import Base  # Переконайтеся, що ви маєте базовий клас для моделей

# Налаштування логування
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Створення асинхронного двигуна з використанням AS_BASE
try:
    engine = create_async_engine(
        settings.db_async_url,
        echo=settings.DEBUG,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20
    )
    logger.info("Async database engine created successfully")
except Exception as e:
    logger.error(f"Failed to create async database engine: {e}")
    raise

# Фабрика асинхронних сесій
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db():
    """Ініціалізація бази даних"""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

async def reset_db():
    """Скидання та створення нової бази даних"""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database reset successfully")
    except Exception as e:
        logger.error(f"Failed to reset database: {e}")
        raise

class DatabaseMiddleware(BaseMiddleware):
    """Middleware для управління сесіями бази даних"""
    def __init__(self, session_factory):
        super().__init__()
        self.session_factory = session_factory

    async def __call__(self, handler, event, data):
        async with self.session_factory() as session:
            data['db'] = session
            try:
                return await handler(event, data)
            except Exception as e:
                logger.error(f"Error in database middleware: {e}")
                await session.rollback()
                raise
            finally:
                await session.close()
