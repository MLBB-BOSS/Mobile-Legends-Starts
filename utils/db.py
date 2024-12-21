#utils/db.py

from utils.charts import create_chart
from utils.charts import charts_router
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from sqlalchemy import select
import logging

from config import settings

logger = logging.getLogger(__name__)

# Створення асинхронного двигуна
engine = create_async_engine(
    settings.AS_BASE,  # Використовуємо AS_BASE замість DB_ASYNC_URL
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

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
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


async def get_user_profile(session: AsyncSession, user_id: int):
    """
    Отримання профілю користувача з бази даних.
    """
    try:
        from models.user import User
        from models.user_stats import UserStats

        # Виконуємо запит до бази даних
        result = await session.execute(
            select(User, UserStats)
            .where(User.telegram_id == user_id)
            .join(UserStats)
        )
        user, stats = result.first()

        # Формуємо результат, якщо користувача знайдено
        if user and stats:
            return {
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
                "last_update": stats.last_update,
            }
        return None

    # Логування у разі помилки
    except Exception as e:
        logger.error(f"Error fetching user profile for user_id {user_id}: {e}")
        return None
