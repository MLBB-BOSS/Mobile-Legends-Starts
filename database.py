from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from aiogram import BaseMiddleware
from config import settings
from models.base import Base
from sqlalchemy.future import select  # Для роботи з профілями користувачів
import logging

# Логування
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Створення асинхронного двигуна
engine = create_async_engine(
    settings.db_async_url,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)
logger.info("Async database engine created successfully")

# Фабрика асинхронних сесій
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db():
    """Ініціалізація бази даних."""
    try:
        async with engine.begin() as conn:
            logger.info("Initializing database...")
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

async def reset_db():
    """Скидання та створення нової бази даних."""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database reset successfully")
    except Exception as e:
        logger.error(f"Failed to reset database: {e}")
        raise

# Функція для отримання профілю користувача
async def get_user_profile(session: AsyncSession, user_id: int):
    """
    Отримання профілю користувача з бази даних.

    :param session: Асинхронна сесія SQLAlchemy.
    :param user_id: Telegram ID користувача.
    :return: Словник з даними профілю або None, якщо користувач не знайдений.
    """
    try:
        from models.user import User
        from models.user_stats import UserStats

        result = await session.execute(
            select(User, UserStats).where(User.telegram_id == user_id).join(UserStats)
        )
        user, stats = result.first()
        if user and stats:
            return {
                "username": user.username,
                "level": stats.level,
                "rating": stats.rating,
                "achievements_count": stats.achievements_count,
                "total_matches": stats.total_matches,
                "total_wins": stats.total_wins,
                "total_losses": stats.total_losses,
                "last_update": stats.last_update,
            }
        return None
    except Exception as e:
        logger.error(f"Error fetching user profile for user_id {user_id}: {e}")
        return None
