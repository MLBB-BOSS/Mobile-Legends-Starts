# utils/db.py
from sqlalchemy.ext.asyncio import AsyncSession
from database import async_session

async def get_db_session() -> AsyncSession:
    async with async_session() as session:
        yield session