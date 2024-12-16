from aiogram import BaseMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from utils.db import async_session
import logging

logger = logging.getLogger(__name__)

class DatabaseMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        logger.info("Initializing database session")
        async with async_session() as session:
            data['db'] = session
            try:
                response = await handler(event, data)
                await session.commit()  # Комміт змін, якщо все успішно
                logger.info("Session committed successfully")
                return response
            except Exception as e:
                logger.error(f"Database error occurred: {e}")
                await session.rollback()  # Відкат змін у разі помилки
                logger.info("Rolled back session due to error")
                raise
            finally:
                await session.close()
                logger.info("Database session closed")
