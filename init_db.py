import asyncio
from utils.db import engine
from models.base import Base
from models.user import User
from models.badge import Badge
from models.user_stats import UserStats

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Таблиці створено успішно.")

if __name__ == "__main__":
    asyncio.run(init_db())
