# database.py
import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from config import settings

# Налаштування логування
logger = logging.getLogger(__name__)

# Створення асинхронного двигуна з використанням db_url
engine = create_async_engine(
    settings.db_url,
    echo=settings.DEBUG,
)

# Фабрика асинхронних сесій, перейменована на async_session
async_session = sessionmaker(
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

class DatabaseMiddleware(BaseMiddleware):
    """
    Middleware для управління сесіями бази даних.
    Відкриває сесію перед обробкою оновлення та закриває після.
    """
    def __init__(self, session_factory):
        super().__init__()
        self.session_factory = session_factory

    async def on_pre_process_message(self, message: Message, data: dict):
        data['db'] = self.session_factory()

    async def on_post_process_message(self, message: Message, result, data: dict):
        db = data.get('db')
        if db:
            await db.close()

    async def on_pre_process_callback_query(self, callback_query: CallbackQuery, data: dict):
        data['db'] = self.session_factory()

    async def on_post_process_callback_query(self, callback_query: CallbackQuery, result, data: dict):
        db = data.get('db')
        if db:
            await db.close()
