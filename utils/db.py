# utils/db.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from utils.models import user, user_stats

async def get_user_profile(db: AsyncSession, telegram_id: int):
    """
    Отримує профіль користувача за його Telegram ID.

    :param db: Асинхронна сесія бази даних.
    :param telegram_id: Telegram ID користувача.
    :return: Об'єкт користувача або None, якщо не знайдено.
    """
    stmt = select(models.user.User).options(selectinload(models.user.User.stats)).where(models.user.User.telegram_id == telegram_id)
    result = await db.execute(stmt)
    user = result.scalars().first()
    if user:
        # Повертаємо словник з потрібними полями
        return {
            "username": user.username,
            "level": user.level,
            "rating": user.rating,
            "achievements_count": user.achievements_count,
            "screenshots_count": user.screenshots_count,
            "missions_count": user.missions_count,
            "quizzes_count": user.quizzes_count,
            "total_matches": user.total_matches,
            "total_wins": user.total_wins,
            "total_losses": user.total_losses,
            "tournament_participations": user.tournament_participations,
            "badges_count": user.badges_count,
            "last_update": user.last_update
        }
    return None