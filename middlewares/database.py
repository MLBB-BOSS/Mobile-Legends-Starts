# middlewares.py

from aiogram.middlewares.base import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession
import logging

logger = logging.getLogger(__name__)

class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, session_factory):
        super().__init__()
        self.session_factory = session_factory

    async def __call__(self, handler, event: TelegramObject, data: dict):
        async with self.session_factory() as session:
            data['db'] = session
            try:
                return await handler(event, data)
            except Exception as e:
                logger.error(f"Database Middleware Error: {e}")
                raise
