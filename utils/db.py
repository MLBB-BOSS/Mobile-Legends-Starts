from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config import settings
import logging

logger = logging.getLogger(__name__)

def create_db_engine():
    """Створення двигунів бази даних з правильними налаштуваннями"""
    # Асинхронний двигун
    async_engine = create_async_engine(
        settings.ASYNC_DATABASE_URL,
        echo=settings.DEBUG,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
        connect_args={
            "connect_timeout": 10,
            "keepalives": 1,
            "keepalives_idle": 30,
            "keepalives_interval": 10,
            "keepalives_count": 5
        }
    )

    # Синхронний двигун
    sync_engine = create_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
        connect_args={
            "connect_timeout": 10,
            "keepalives": 1,
            "keepalives_idle": 30,
            "keepalives_interval": 10,
            "keepalives_count": 5
        }
    )

    return async_engine, sync_engine

# Створюємо двигуни
engine, sync_engine = create_db_engine()

# Створюємо фабрику сесій
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db():
    """Ініціалізація бази даних"""
    try:
        # Тестуємо підключення
        async with engine.connect() as conn:
            await conn.execute("SELECT 1")
            logger.info("Database connection test successful")
    except Exception as e:
        logger.error(f"Database initialization error: {str(e)}")
        raise

async def get_session() -> AsyncSession:
    """Отримання сесії бази даних"""
    async with async_session() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            logger.error(f"Database session error: {str(e)}")
            raise
        finally:
            await session.close()
