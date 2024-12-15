import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from aiogram import BaseMiddleware
from config import settings

# Створення базового класу для моделей
Base = declarative_base()

class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, session_factory):
        super().__init__()
        self.session_factory = session_factory

    async def __call__(self, handler, event, data):
        async with self.session_factory() as session:
            data['db'] = session
            try:
                return await handler(event, data)
            except Exception as e:
                await session.rollback()
                raise
            finally:
                await session.close()

# Створення асинхронного двигуна
engine = create_async_engine(
    settings.db_url,
    echo=settings.DEBUG,
    pool_size=10,
    max_overflow=20
)

# Фабрика асинхронних сесій
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Змінна середовища або хардкоджений URL — краще зберігати у змінних середовища
AS_BASE = os.getenv("AS_BASE", "postgresql+asyncpg://user:password@host:port/dbname")

if not AS_BASE:
    raise ValueError("AS_BASE is not set or invalid")

engine = create_async_engine(AS_BASE, echo=False)

# Оновлена фабрика сесій
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Функція для отримання асинхронної сесії
async def get_db_session() -> AsyncSession:
    async with async_session() as session:
        yield session