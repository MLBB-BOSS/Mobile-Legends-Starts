# database/connection.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config.settings import settings

DATABASE_URL = settings.ASYNC_DATABASE_URL or settings.DATABASE_URL

# Створення асинхронного engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Створення sessionmaker
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    """Функція для отримання сесії бази даних"""
    async with AsyncSessionLocal() as session:
        yield session
