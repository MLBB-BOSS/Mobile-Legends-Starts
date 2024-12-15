import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from models.base import Base
from config import settings

async def init_db():
    """Ініціалізація бази даних: створення таблиць."""
    engine = create_async_engine(settings.db_url, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database initialized successfully.")

if __name__ == "__main__":
    asyncio.run(init_db())