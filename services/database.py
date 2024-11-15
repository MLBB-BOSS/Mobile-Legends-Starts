from typing import Optional, AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, text
import logging
from datetime import datetime
from core.config import settings

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

# Створюємо базовий клас для моделей
Base = declarative_base()

# Створюємо підключення до бази даних
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_timeout=settings.DB_POOL_TIMEOUT
)

# Створюємо фабрику сесій
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Генератор асинхронних сесій для роботи з БД"""
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Помилка сесії БД: {e}")
            raise
        finally:
            await session.close()

async def init_db() -> bool:
    """Ініціалізація бази даних"""
    try:
        async with engine.begin() as conn:
            # Перевіряємо підключення
            await conn.execute(text("SELECT 1"))
            logger.info("Підключення до бази даних встановлено")

            # Перевіряємо існування таблиць
            check_query = text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'users'
                )
            """)
            result = await conn.execute(check_query)
            exists = await result.scalar()

            if not exists:
                logger.info("Створюємо таблиці...")
                await conn.run_sync(Base.metadata.create_all)
                logger.info("Таблиці успішно створені")
            else:
                logger.info("Таблиці вже існують")

            return True

    except Exception as e:
        logger.error(f"Помилка при ініціалізації бази даних: {str(e)}")
        return False
