# database/connection.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config.settings import settings
from database.base import Base  # Імпорт базового класу для моделей
import asyncio

# Встановлення URL для підключення до бази даних
DATABASE_URL = settings.ASYNC_DATABASE_URL or settings.DATABASE_URL

# Створення асинхронного engine для роботи з базою даних
engine = create_async_engine(DATABASE_URL, echo=True)

# Створення sessionmaker для асинхронної сесії
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db():
    """Ініціалізація бази даних - створення таблиць з моделей, якщо їх немає"""
    async with engine.begin() as conn:
        # Створює всі таблиці, визначені в моделях, якщо їх ще немає в базі
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    """Функція для отримання сесії бази даних"""
    async with AsyncSessionLocal() as session:
        yield session

# Додайте цей код для одноразового створення таблиць
# Запускати тільки локально або на Heroku, поки таблиці не створені
if __name__ == "__main__":
    asyncio.run(init_db())
