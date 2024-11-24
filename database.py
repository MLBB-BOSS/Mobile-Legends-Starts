from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from config import settings
from typing import AsyncGenerator

DATABASE_URL = settings.async_database_url

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)
Base = declarative_base()

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

async def create_db_and_tables():
    async with engine.begin() as conn:
        # Імпортуємо моделі тут, щоб уникнути циклічних імпортів
        from models import User  # noqa
        
        # Створюємо таблиці
        await conn.run_sync(Base.metadata.create_all)
