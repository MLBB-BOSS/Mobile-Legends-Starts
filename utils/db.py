from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings
import logging

logger = logging.getLogger(__name__)

# Базовий клас для моделей
Base = declarative_base()

# Асинхронний двигун SQLAlchemy
async_engine: AsyncEngine = create_async_engine(
    settings.db_async_url,
    echo=settings.DEBUG,
    future=True,
)

# Синхронний двигун SQLAlchemy
from sqlalchemy import create_engine

sync_engine = create_engine(
    settings.db_sync_url,
    echo=settings.DEBUG,
    future=True,
)

# Асинхронна сесія
async_session = sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession
)

# Синхронна сесія
SessionLocal = sessionmaker(
    bind=sync_engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)

async def init_db():
    """Ініціалізує базу даних, створюючи всі таблиці."""
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Async Database tables created successfully")
    except Exception as e:
        logger.error(f"Error initializing async database: {e}")
        raise