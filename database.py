# database.py

import logging
from typing import Callable, Any

from aiogram.dispatcher.middlewares import BaseMiddleware
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from config import settings  # Ваш файл конфігурації

logger = logging.getLogger(__name__)

# Ініціалізація бази даних
DATABASE_URL = settings.DATABASE_URL  # Переконайтесь, що цей URL правильний

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

Base = declarative_base()

class DatabaseMiddleware(BaseMiddleware):
    """Middleware для інжекції сесії бази даних у обробники."""

    def __init__(self, session_factory: Callable[[], AsyncSession]):
        super().__init__()
        self.session_factory = session_factory

    async def __call__(
        self,
        handler: Callable[[Any], Any],
        event: Any,
        data: dict
    ) -> Any:
        async with self.session_factory() as session:
            data['db'] = session  # Інжектимо сесію у data
            try:
                return await handler(event, data)
            except Exception as e:
                logger.error(f"Помилка в DatabaseMiddleware: {e}")
                await session.rollback()
                raise
