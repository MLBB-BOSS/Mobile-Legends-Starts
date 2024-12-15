import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models.base import Base

# URL бази даних
DATABASE_URL = os.getenv("AS_BASE", "postgresql+asyncpg://user:password@host:port/dbname")

if not DATABASE_URL:
    raise ValueError("AS_BASE is not set or invalid")

# Створення асинхронного двигуна
engine = create_async_engine(DATABASE_URL, echo=True)

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