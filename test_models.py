# test_models.py
import asyncio
import logging
from database import engine
from models import Base  # Імпортуємо базу даних та всі моделі через models/__init__.py

async def test():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # Очистити існуючі таблиці
        await conn.run_sync(Base.metadata.create_all)  # Створити таблиці заново
    logging.info("Таблиці успішно створено.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(test())