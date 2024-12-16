import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager

# URL бази даних (краще зберігати у змінних середовища)
AS_BASE = os.getenv(
    "AS_BASE", 
    "postgresql+asyncpg://udoepvnsfd1v4p:p06d554a757b594fc448b0fe17f59b24af6e1ed553f9cd262a36d4e56fd87a37f@c9tiftt16dc3eo.cluster-czz5s0kz4scl.eu-west-1.rds.amazonaws.com:5432/d76pc5iknkd84"
)

if not AS_BASE:
    raise ValueError("AS_BASE is not set or invalid")

# Ініціалізація асинхронного двигуна для роботи з базою даних
engine = create_async_engine(AS_BASE, echo=False)

# Налаштування фабрики для створення сесій
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Функція для отримання сесії бази даних
@asynccontextmanager
async def get_db_session() -> AsyncSession:
    async with async_session() as session:
        yield session
