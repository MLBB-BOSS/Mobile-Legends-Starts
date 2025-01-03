# utils/db.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
import logging

from utils.base import Base
from utils.models import User
from utils.settings import settings

logger = logging.getLogger(__name__)

# Створення асинхронного двигуна
async_engine = create_async_engine(
    settings.ASYNC_DATABASE_URL,
    echo=settings.DEBUG,
    future=True
)

# Створення фабрики сесій
async_session = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db():
    """Ініціалізація бази даних"""
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("База даних успішно ініціалізована")
    except Exception as e:
        logger.error(f"Помилка при ініціалізації бази даних: {e}")
        raise

async def get_user_profile(user_id: int) -> dict:
    """
    Отримання профілю користувача
    
    Args:
        user_id (int): ID користувача Telegram
        
    Returns:
        dict: Словник з даними профілю користувача
    """
    try:
        async with async_session() as session:
            # Отримуємо користувача
            query = select(User).where(User.id == user_id)
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            
            if not user:
                return None
            
            # Формуємо профіль
            profile = {
                "id": user.id,
                "username": user.username,
                "created_at": user.created_at,
                "tournaments_count": await get_user_tournaments_count(session, user_id),
                "wins": await get_user_wins_count(session, user_id),
                "rating": await calculate_user_rating(session, user_id)
            }
            
            return profile
            
    except Exception as e:
        logger.error(f"Помилка при отриманні профілю користувача {user_id}: {e}")
        return None

async def get_user_tournaments_count(session: AsyncSession, user_id: int) -> int:
    """Отримання кількості турнірів користувача"""
    # TODO: Реалізувати підрахунок турнірів
    return 0

async def get_user_wins_count(session: AsyncSession, user_id: int) -> int:
    """Отримання кількості перемог користувача"""
    # TODO: Реалізувати підрахунок перемог
    return 0

async def calculate_user_rating(session: AsyncSession, user_id: int) -> float:
    """Розрахунок рейтингу користувача"""
    # TODO: Реалізувати розрахунок рейтингу
    return 0.0
