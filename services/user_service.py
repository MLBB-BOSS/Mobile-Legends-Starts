from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from models.user import User
from models.user_stats import UserStats
from sqlalchemy.ext.asyncio import AsyncSession
import logging

logger = logging.getLogger(__name__)

async def get_or_create_user(db: AsyncSession, telegram_id: int, username: str) -> User:
    """
    Отримує або створює користувача за telegram_id.
    """
    result = await db.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalars().first()

    if not user:
        # Створюємо нового користувача
        user = User(telegram_id=telegram_id, username=username)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        logger.info(f"Створено нового користувача з telegram_id={telegram_id}")
    return user

async def get_user_profile_text(db: AsyncSession, telegram_id: int, username: str) -> str:
    """
    Формує текст профілю користувача.
    """
    try:
        # Отримуємо або створюємо користувача
        user = await get_or_create_user(db, telegram_id, username)

        # Отримуємо статистику
        result = await db.execute(select(UserStats).where(UserStats.user_id == user.id))
        stats = result.scalars().first()

        # Якщо статистики немає, створюємо базову
        if not stats:
            stats = UserStats(user_id=user.id, rating=100, achievements_count=0, total_matches=0, total_wins=0, total_losses=0)
            db.add(stats)
            await db.commit()
            await db.refresh(stats)

        # Формуємо текст профілю
        profile_text = (
            f"🔍 **Ваш Профіль:**\n\n"
            f"• 🏅 Ім'я користувача: @{user.username or 'Невідомо'}\n"
            f"• 🚀 Рейтинг: {stats.rating}\n"
            f"• 🎯 Досягнення: {stats.achievements_count} досягнень\n"
            f"• 🎮 Матчі: {stats.total_matches}, Перемоги: {stats.total_wins}, Поразки: {stats.total_losses}\n"
        )

        # Додаємо інформацію про останнє оновлення, якщо вона є
        if stats.last_update:
            profile_text += f"• 🕒 Останнє оновлення: {stats.last_update.strftime('%Y-%m-%d %H:%M:%S')}"

        return profile_text
    except SQLAlchemyError as e:
        logger.error(f"Error fetching user profile for telegram_id={telegram_id}: {e}")
        return "⚠️ Виникла помилка при отриманні профілю. Спробуйте пізніше."