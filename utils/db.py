# utils/db.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

AS_BASE = "postgresql+asyncpg://user:password@host:port/dbname"

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_db_session() -> AsyncSession:
    # Повертає нову сесію БД
    return async_session()
