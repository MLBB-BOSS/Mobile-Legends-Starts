from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
import logging
from core.config import settings

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    pass

# Create async engine
engine = create_async_engine(
    settings.ASYNC_DATABASE_URL,
    echo=settings.DEBUG,
    future=True
)

# Create session factory
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            await session.close()

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
