# utils/db.py

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from models.user_stats import UserStats
import logging

logger = logging.getLogger(__name__)

async def get_or_create_user(db: AsyncSession, telegram_id: int, user_data: dict):
    """
    Перевіряє, чи існує користувач у базі. Якщо ні — створює його.

    :param db: Асинхронна сесія бази даних.
    :param telegram_id: Telegram ID користувача.
    :param user_data: Словник з даними користувача.
    :return: Кортеж (User, bool), де bool означає, чи був створений новий користувач.
    """
    try:
        # Перевірка наявності користувача
        query = select(User).where(User.telegram_id == telegram_id)
        result = await db.execute(query)
        user = result.scalars().first()

        if not user:
            # Створення нового користувача
            user = User(
                telegram_id=telegram_id,
                username=user_data.get("username"),
                first_name=user_data.get("first_name"),
                last_name=user_data.get("last_name"),
                language_code=user_data.get("language_code")
            )
            db.add(user)
            await db.flush()  # Необхідно для отримання ID нового користувача

            # Створення запису статистики для нового користувача
            new_stats = UserStats(user_id=user.id)
            db.add(new_stats)

            await db.commit()
            logger.info(f"Зареєстровано нового користувача: {telegram_id}")
            return user, True  # Новий користувач
        else:
            logger.info(f"Існуючий користувач: {telegram_id}")
            return user, False  # Існуючий користувач
    except Exception as e:
        logger.error(f"Помилка при отриманні або створенні користувача {telegram_id}: {e}")
        await db.rollback()
        raise

async def get_user_profile(db: AsyncSession, telegram_id: int) -> Optional[Dict[str, any]]:
    """
    Отримує профіль користувача з бази даних.

    :param db: Асинхронна сесія бази даних.
    :param telegram_id: Telegram ID користувача.
    :return: Словник з даними профілю або None, якщо користувача не знайдено.
    """
    try:
        query = select(User).where(User.telegram_id == telegram_id)
        result = await db.execute(query)
        user = result.scalars().first()

        if not user:
            logger.warning(f"Користувача з Telegram ID {telegram_id} не знайдено.")
            return None

        # Отримуємо статистику користувача
        stats = user.stats
        if not stats:
            logger.warning(f"Статистика користувача {telegram_id} не знайдена.")
            return None

        profile_data = {
            "username": user.username,
            "level": stats.level,
            "rating": stats.rating,
            "achievements_count": stats.achievements_count,
            "screenshots_count": stats.screenshots_count,
            "missions_count": stats.missions_count,
            "quizzes_count": stats.quizzes_count,
            "total_matches": stats.total_matches,
            "total_wins": stats.total_wins,
            "total_losses": stats.total_losses,
            "tournament_participations": stats.tournament_participations,
            "badges_count": stats.badges_count,
            "last_update": stats.last_update
        }

        return profile_data
    except Exception as e:
        logger.error(f"Помилка при отриманні профілю користувача {telegram_id}: {e}")
        await db.rollback()
        return None