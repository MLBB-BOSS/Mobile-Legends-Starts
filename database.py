# database.py
import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from aiogram import BaseMiddleware
from config import settings

logger = logging.getLogger(__name__)

try:
    engine = create_async_engine(
        settings.db_url,
        echo=settings.DEBUG,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20
    )
    logger.info("Database engine created successfully")
except Exception as e:
    logger.error(f"Failed to create database engine: {e}")
    raise

# async_session – це sessionmaker, виклик async_session() створює нову AsyncSession
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db():
    from models.base import Base
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

async def reset_db():
    from models.base import Base
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database reset successfully")
    except Exception as e:
        logger.error(f"Failed to reset database: {e}")
        raise

class DatabaseMiddleware(BaseMiddleware):
    """Middleware для керування сесіями бази даних"""
    def __init__(self, session_factory):
        super().__init__()
        # session_factory тепер буде async_session (sessionmaker), який при виклику
        # session_factory() дасть нам AsyncSession
        self.session_factory = session_factory

    async def __call__(self, handler, event, data):
        # Виклик session_factory(): async_session() → AsyncSession
        # AsyncSession підтримує async with
        async with self.session_factory() as session:
            data['db'] = session
            try:
                return await handler(event, data)
            except Exception as e:
                logger.error(f"Error in database middleware: {e}")
                await session.rollback()
                raise
