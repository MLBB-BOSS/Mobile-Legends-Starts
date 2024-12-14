# test_models.py
import asyncio
from database import engine
from models.base import Base
import models.user
import models.badge
import models.user_stats
import models.user_badges

async def test():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # Очистити існуючі таблиці
        await conn.run_sync(Base.metadata.create_all)  # Створити таблиці заново
    print("Таблиці успішно створено.")

if __name__ == "__main__":
    asyncio.run(test())
