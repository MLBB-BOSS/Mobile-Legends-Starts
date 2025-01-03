# utils/db.py
import logging
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, Session

from .models import Base
from .settings import settings

logger = logging.getLogger(__name__)

# Налаштування двигунів
async_engine = create_async_engine(
    settings.ASYNC_DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW
)

sync_engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW
)

# Фабрики сесій
async_session = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

sync_session = sessionmaker(
    sync_engine,
    class_=Session,
    expire_on_commit=False
)

# Ініціалізація баз даних
async def init_db():
    """Ініціалізація асинхронної бази даних"""
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Асинхронна база даних успішно ініціалізована")
    except Exception as e:
        logger.error(f"Помилка при ініціалізації асинхронної бази даних: {e}")
        raise

def init_sync_db():
    """Ініціалізація синхронної бази даних"""
    try:
        Base.metadata.create_all(sync_engine)
        logger.info("Синхронна база даних успішно ініціалізована")
    except Exception as e:
        logger.error(f"Помилка при ініціалізації синхронної бази даних: {e}")
        raise

@contextmanager
def get_sync_db():
    """Контекстний менеджер для синхронної сесії"""
    session = sync_session()
    try:
        yield session
    finally:
        session.close()

async def get_async_db():
    """Асинхронний контекстний менеджер для асинхронної сесії"""
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

# Допоміжні функції для роботи з базою даних
async def get_or_create_user(user_id: int, username: str):
    """Отримати або створити користувача"""
    async with async_session() as session:
        async with session.begin():
            user = await session.get(User, user_id)
            if not user:
                user = User(
                    id=user_id,
                    username=username
                )
                session.add(user)
                await session.commit()
            return user
