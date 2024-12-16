import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from aiogram import BaseMiddleware
from config import settings
from models.user import User

# Налаштування логування
logger = logging.getLogger(__name__)

# Створення асинхронного двигуна з використанням db_url
try:
    engine = create_async_engine(
        settings.db_url,
        echo=settings.DEBUG,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20
    )
    logger.info("Database engine created successfully")
except Exception as e:
    logger.error(f"Failed to create database engine: {e}")
    raise

# Фабрика асинхронних сесій
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db():
    """Ініціалізація бази даних"""
    from models.base import Base
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

async def reset_db():
    """Скидання та створення нової бази даних"""
    from models.base import Base
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database reset successfully")
    except Exception as e:
        logger.error(f"Failed to reset database: {e}")
        raise

# Функції для роботи з користувачами
async def get_user(session: AsyncSession, telegram_id: int) -> User | None:
    """Отримує користувача за Telegram ID."""
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    return result.scalar_one_or_none()

async def create_user(session: AsyncSession, telegram_id: int, username: str = None) -> User:
    """Створює нового користувача."""
    user = User(telegram_id=telegram_id, username=username)
    session.add(user)
    await session.flush()
    return user

class DatabaseMiddleware(BaseMiddleware):
    """Middleware для управління сесіями бази даних"""
    def __init__(self, session_factory):
        super().__init__()
        self.session_factory = session_factory

    async def __call__(self, handler, event, data):
        async with self.session_factory() as session:
            data['db'] = session
            try:
                return await handler(event, data)
            except Exception as e:
                logger.error(f"Error in database middleware: {e}")
                await session.rollback()
                raise
            finally:
                await session.close()