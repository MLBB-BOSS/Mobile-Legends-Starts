# utils/db.py
from sqlalchemy.ext.asyncio import AsyncSession
from database import async_session
from contextlib import asynccontextmanager

@asynccontextmanager
async def get_db_session():
    async with async_session() as session:
        yield session
