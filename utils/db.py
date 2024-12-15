import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Базовий клас для моделей
from models.base import Base

# URL бази даних
DATABASE_URL = os.getenv("AS_BASE", "postgresql+asyncpg://ufk3frgco7l9d1:p7aad477be5e7c084f8d9c2e9998fdfd75ed3eb573c808a6b3db95bbdb221b234@ccaml3dimis7eh.cluster-czz5s0kz4scl.eu-west-1.rds.amazonaws.com:5432/d7rglea9jc6ggd")

if not DATABASE_URL:
    raise ValueError("AS_BASE is not set or invalid")

# Створення асинхронного двигуна
engine = create_async_engine(DATABASE_URL, echo=True)

# Фабрика асинхронних сесій
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Middleware для роботи з базою даних
class DatabaseMiddleware:
    def __init__(self, session_factory):
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