from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
import logging

from config import settings

logger = logging.getLogger(__name__)

# Створення асинхронного двигуна
engine = create_async_engine(
    settings.AS_BASE,  # Використовуємо AS_BASE для асинхронного з'єднання
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
        from sqlalchemy import select
        from models.user import User
        from models.user_stats import UserStats

        result = await session.execute(
            select(User, UserStats)
            .where(User.telegram_id == user_id)
            .join(UserStats)
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
