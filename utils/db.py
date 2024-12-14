# utils/db.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://user:password@host:port/dbname"

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_db_session() -> AsyncSession:
    # Повертає асинхронну сесію. 
    # Залежно від вашої логіки, можливо вам потрібно використати контекстний менеджер async with:
    session = async_session()
    return session
