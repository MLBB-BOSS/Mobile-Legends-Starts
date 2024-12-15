import asyncio
import logging
from utils.db import engine
from models.base import Base
import models.user  # Імпортуємо модель User
import models.user_stats  # Імпортуємо модель UserStats

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("init_db")

async def init_db():
    """Ініціалізація бази даних: створення таблиць."""
    try:
        logger.info("Starting database initialization...")
        async with engine.begin() as conn:
            # Видаляємо існуючі таблиці (опціонально)
            # await conn.run_sync(Base.metadata.drop_all)

            # Створюємо нові таблиці
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Error during database initialization: {e}")
        raise

if __name__ == "__main__":
    try:
        asyncio.run(init_db())
    except Exception as e:
        logger.critical(f"Critical error initializing the database: {e}")
        raise


import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

# Базовий клас для моделей
Base = declarative_base()

# URL бази даних
DATABASE_URL = os.getenv("AS_BASE", "postgresql+asyncpg://user:password@host:port/dbname")

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


import io
import matplotlib.pyplot as plt
from aiogram import Router
from aiogram.types import Message, InputFile
from aiogram.filters import Command

router = Router()

# Функція для генерації графіка
def generate_rating_chart(rating_history: list[int]) -> io.BytesIO:
    """
    Генерує графік зміни рейтингу.
    rating_history - список рейтингів по часу, наприклад: [100, 200, 250, 300].
    """
    plt.figure(figsize=(4, 4))
    plt.plot(rating_history, marker='o')
    plt.title("Графік зміни рейтингу")
    plt.xlabel("Сеанс")
    plt.ylabel("Рейтинг")
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return buf

# Обробник команди
@router.message(Command("my_progress"))
async def show_progress(message: Message):
    rating_history = [100, 200, 250, 300]  # Зразкові дані
    chart = generate_rating_chart(rating_history)  # Генеруємо графік

    # Обгортаємо BytesIO в InputFile
    photo_file = InputFile(chart, filename="chart.png")
    profile_text = "Ваш прогрес за останні сеанси"

    # Відправляємо графік
    await message.answer_photo(photo=photo_file, caption=profile_text)


# models/base.py

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Base(AsyncAttrs, DeclarativeBase):
    """Base class for all models"""

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in self.__table__.columns}


# models/base.py
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs

class Base(AsyncAttrs, DeclarativeBase):
    """Base class for all models"""
    
    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in self.__table__.columns}


Database
d7rglea9jc6ggd
User
ufk3frgco7l9d1
Port
5432


# models/base.py
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs

class Base(AsyncAttrs, DeclarativeBase):
    """Base class for all models"""
    
    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in self.__table__.columns}


Database
d7rglea9jc6ggd
User
ufk3frgco7l9d1
Port
5432



AS_BASEpostgresql+asyncpg://ufk3frgco7l9d1:p7aad477be5e7c084f8d9c2e9998fdfd75ed3eb573c808a6b3db95bbdb221b234@ccaml3dimis7eh.cluster-czz5s0kz4scl.eu-west-1.rds.amazonaws.com:5432/d7rglea9jc6ggd