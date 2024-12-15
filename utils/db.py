import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models.base import Base

# URL бази даних
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@host:port/dbname")

# Створення асинхронного двигуна
engine = create_async_engine(DATABASE_URL, echo=False)

# Фабрика асинхронних сесій
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Функція для створення таблиць
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Функція для отримання сесії
async def get_db_session():
    async with async_session() as session:
        yield session