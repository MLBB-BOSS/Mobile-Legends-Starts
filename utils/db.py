
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Завантажуємо змінні оточення
load_dotenv()

# Базовий клас для моделей
from models.base import Base

# URL бази даних
DATABASE_URL = os.getenv("AS_BASE")

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