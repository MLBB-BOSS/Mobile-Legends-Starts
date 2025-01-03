# utils/db.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from utils.models import User, UserStats

async def get_user(db: AsyncSession, telegram_id: int) -> User | None:
    result = await db.execute(select(User).where(User.telegram_id == telegram_id))
    return result.scalar_one_or_none()

async def get_user_profile(db: AsyncSession, telegram_id: int):
    user = await get_user(db, telegram_id)
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

async def create_user(db: AsyncSession, telegram_id: int, username: str = None) -> User:
    user = User(telegram_id=telegram_id, username=username)
    db.add(user)
    await db.flush()
    return user

async def get_or_create_user_stats(db: AsyncSession, user: User) -> UserStats:
    result = await db.execute(select(UserStats).where(UserStats.user_id == user.id))
    stats = result.scalar_one_or_none()
    if not stats:
        stats = UserStats(user_id=user.id)
        db.add(stats)
        await db.flush()
    return stats

async def update_user_stats(db: AsyncSession, telegram_id: int, rating: int = None, achievements: int = None) -> None:
    user = await get_user(db, telegram_id)
    if not user:
        user = await create_user(db, telegram_id)
    stats = await get_or_create_user_stats(db, user)
    if rating is not None:
        stats.rating = rating
    if achievements is not None:
        stats.achievements_count = achievements
    stats.last_update = datetime.utcnow()
    await db.commit()
