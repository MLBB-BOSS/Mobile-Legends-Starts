from aiogram import BaseMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from utils.db import async_session
import logging

logger = logging.getLogger(__name__)

class DatabaseMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        async with async_session() as session:
            data['db'] = session
            try:
                return await handler(event, data)
            except Exception as e:
                logger.error(f"Database error: {e}")
                await session.rollback()
                raise
            finally:
                await session.close()
