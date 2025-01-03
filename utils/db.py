from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from models.user import User
from models.user_stats import UserStats
import logging
from config import settings  # Імпорт з кореневої директорії
from utils.db_base import Base

logger = logging.getLogger(__name__)

# Створення асинхронного двигуна
engine = create_async_engine(
    settings.AS_BASE,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW
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
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

async def get_session() -> AsyncSession:
    """Отримання сесії бази даних."""
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

async def check_connection():
    """Перевірка з'єднання з базою даних."""
    try:
        async with async_session() as session:
            await session.execute("SELECT 1")
        logger.info("Database connection test successful")
        return True
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        return False

async def get_user_profile(session: AsyncSession, telegram_id: int) -> dict:
    user = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user = user.scalar_one_or_none()
    if not user:
        return None

    user_stats = await session.execute(select(UserStats).where(UserStats.user_id == user.id))
    user_stats = user_stats.scalar_one_or_none()
    
    return {
        "username": user.username,
        "level": user_stats.rating // 100,
        "rating": user_stats.rating,
        "achievements_count": user_stats.achievements_count,
        "screenshots_count": user_stats.total_screenshots,
        "missions_count": user_stats.missions_count,
        "quizzes_count": user_stats.quizzes_count,
        "total_matches": user_stats.matches_played,
        "total_wins": user_stats.matches_won,
        "total_losses": user_stats.matches_played - user_stats.matches_won,
        "tournament_participations": user_stats.tournaments_played,
        "badges_count": user_stats.achievements_count,
        "last_update": user_stats.last_activity
    }