# utils/db.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from database import async_session  # Припустимо, ви імпортуєте sessionmaker з database.py

async def get_db_session() -> AsyncSession:
    """
    Повертає нову асинхронну сесію для роботи з базою даних.
    Використовується при кожному зверненні до бази, якщо ви не використовуєте middleware.
    """
    async with async_session() as session:
        yield session