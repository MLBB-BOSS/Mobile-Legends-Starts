# services/database.py
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import text
import logging
from core.config import settings

# Налаштування логування
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

# Створюємо базовий клас для моделей
Base = declarative_base()

# Створюємо підключення до бази даних
engine = create_async_engine(str(settings.DATABASE_URL))

# Створюємо фабрику сесій
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

async def init_db() -> bool:
    """Ініціалізація бази даних"""
    try:
        async with engine.begin() as conn:
            # Перевіряємо підключення
            await conn.execute(text("SELECT 1"))
            logger.info("Database connection established")
            
            # Створюємо таблиці
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables created successfully")
            return True
    except Exception as e:
        logger.error(f"Database initialization error: {e}")
        return False
