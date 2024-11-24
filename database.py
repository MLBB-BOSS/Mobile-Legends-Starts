# database.py

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator, Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from config import settings

# Налаштування бази даних
DATABASE_URL = settings.async_database_url
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)
Base = declarative_base()

# Функція для отримання сесії
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

# Middleware для бази даних
class DatabaseMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        async for session in get_session():
            data['session'] = session
            try:
                return await handler(event, data)
            finally:
                await session.close()

# Функція для створення таблиць
async def create_db_and_tables():
    async with engine.begin() as conn:
        # Імпортуємо моделі тут, щоб уникнути циклічних імпортів
        from models.user import User  # noqa
        
        await conn.run_sync(Base.metadata.create_all)
