from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os

# URL бази даних
AS_BASE = os.getenv(
    "AS_BASE",
    "postgresql+asyncpg://user:password@host:port/database"
)

# Ініціалізація двигуна
engine = create_async_engine(AS_BASE, echo=True)

# Фабрика сесій
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_db_session() -> AsyncSession:
    """Функція для отримання сесії бази даних."""
    return async_session()