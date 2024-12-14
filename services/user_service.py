from sqlalchemy import select
from models.user import User
from models.user_stats import UserStats
from datetime import datetime

async def get_user(session, telegram_id: int) -> User:
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    return result.scalar_one_or_none()

async def create_user(session, telegram_id: int, username: str = None) -> User:
    user = User(telegram_id=telegram_id, username=username)
    session.add(user)
    await session.flush()
    return user

async def get_or_create_user_stats(session, user: User) -> UserStats:
    result = await session.execute(select(UserStats).where(UserStats.user_id == user.id))
    stats = result.scalar_one_or_none()
    if not stats:
        stats = UserStats(user_id=user.id)
        session.add(stats)
        await session.flush()
    return stats

async def update_user_stats(session, telegram_id: int, rating: int = None, achievements: int = None):
    user = await get_user(session, telegram_id)
    if not user:
        user = await create_user(session, telegram_id)
    stats = await get_or_create_user_stats(session, user)
    if rating is not None:
        stats.rating = rating
    if achievements is not None:
        stats.achievements_count = achievements
    stats.last_update = datetime.utcnow()
    await session.commit()

async def get_user_profile_text(session, telegram_id: int) -> str:
    user = await get_user(session, telegram_id)
    if not user:
        return "Користувач не знайдений."

    stats = await get_or_create_user_stats(session, user)
    # Припустимо, рівень користувача ми обраховуємо за рейтингом:
    level = stats.rating // 100  # Кожні 100 рейтингу - новий рівень

    profile_text = (
        f"🔎 <b>Ваш Профіль:</b>\n\n"
        f"🏅 Ім'я користувача: <b>{user.username or 'Невідомо'}</b>\n"
        f"🚀 Рівень: <b>{level}</b>\n"
        f"📈 Рейтинг: <b>{stats.rating}</b>\n"
        f"🎯 Досягнення: <b>{stats.achievements_count} досягнень</b>\n"
        f"🎮 Матчі: {stats.total_matches}, Перемоги: {stats.total_wins}, Поразки: {stats.total_losses}\n"
        f"\nОстаннє оновлення: {stats.last_update.strftime('%Y-%m-%d %H:%M:%S')}"
    )
    return profile_text
