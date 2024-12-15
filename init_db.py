import asyncio
from database import engine
from models.base import Base

async def init_db():
    """Ініціалізація бази даних: створення таблиць."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database initialized successfully.")

if __name__ == "__main__":
    asyncio.run(init_db())