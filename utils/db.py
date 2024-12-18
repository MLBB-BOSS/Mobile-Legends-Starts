# utils/db.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user import User
from models.user_stats import UserStats
import logging

logger = logging.getLogger(__name__)

async def get_user_profile(session: AsyncSession, user_id: int):
    """
    Отримання профілю користувача з бази даних.
    """
    try:
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