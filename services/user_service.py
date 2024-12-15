# services/user_service.py
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from models.user import User
from models.user_stats import UserStats
from sqlalchemy.ext.asyncio import AsyncSession
import logging

logger = logging.getLogger(__name__)

async def get_or_create_user(db: AsyncSession, telegram_id: int, username: str) -> User:
    # Спробуємо знайти користувача
    result = await db.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalars().first()

    if not user:
        # Користувача не знайдено — створимо нового
        user = User(telegram_id=telegram_id, username=username)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        logger.info(f"Створено нового користувача з telegram_id={telegram_id}")
    return user

async def get_user_profile_text(db: AsyncSession, telegram_id: int, username: str) -> str:
    try:
        # Виклик get_or_create_user щоб завжди мати користувача
        user = await get_or_create_user(db, telegram_id, username)

        # Отримання статистики користувача
        result = await db.execute(select(UserStats).where(UserStats.user_id == user.id))
        stats = result.scalars().first()

        if not stats:
            # Якщо статистики нема — можна створити базову статистику
            stats = UserStats(user_id=user.id, rating=100, achievements_count=0)
            db.add(stats)
            await db.commit()
            await db.refresh(stats)

        profile_text = (
            f"🔍 **Ваш Профіль:**\n\n"
            f"• 🏅 Ім'я користувача: @{user.username}\n"
            f"• 📈 Рейтинг: {stats.rating}\n"
            f"• 🎯 Досягнення: {stats.achievements_count} досягнень"
        )
        return profile_text
    except SQLAlchemyError as e:
        logger.error(f"Error fetching user profile for telegram_id={telegram_id}: {e}")
        return "Виникла помилка при отриманні профілю. Спробуйте пізніше."