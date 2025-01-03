from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.future import select
from contextlib import asynccontextmanager
import logging

from .config import settings
from .models import Base, User, UserStats

# Налаштування логування
logger = logging.getLogger(__name__)

# Створення двигунів
async_engine = create_async_engine(
    settings.ASYNC_DATABASE_URL,
    echo=settings.DB_ECHO,
    pool_pre_ping=True,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW
)

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,
    pool_pre_ping=True,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW
)

# Створення сесій
async_session = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

sync_session = sessionmaker(
    bind=engine,
    expire_on_commit=False
)

@asynccontextmanager
async def get_async_session():
    """Асинхронний контекстний менеджер для сесії"""
    session = async_session()
    try:
        yield session
    finally:
        await session.close()

async def init_db():
    """Ініціалізація бази даних"""
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise

async def get_user_profile(user_id: int) -> dict:
    """Отримання профілю користувача"""
    try:
        async with get_async_session() as session:
            result = await session.execute(
                select(User, UserStats)
                .join(UserStats, User.id == UserStats.user_id)
                .where(User.id == user_id)
            )
            user, stats = result.first()
            
            if not user or not stats:
                return None
                
            return {
                "username": user.username,
                "created_at": user.created_at,
                "rating": user.rating,
                "tournaments_count": user.tournaments_count,
                "wins": user.wins,
                "matches_count": user.matches_count,
                "achievements_count": stats.achievements_count,
                "last_activity": stats.last_activity
            }
    except Exception as e:
        logger.error(f"Error fetching user profile for user_id {user_id}: {e}")
        return None

async def create_user(user_id: int, username: str) -> User:
    """Створення нового користувача"""
    try:
        async with get_async_session() as session:
            user = User(
                id=user_id,
                username=username
            )
            session.add(user)
            
            # Створюємо статистику для користувача
            stats = UserStats(user_id=user_id)
            session.add(stats)
            
            await session.commit()
            await session.refresh(user)
            return user
    except Exception as e:
        logger.error(f"Error creating user {username} (ID: {user_id}): {e}")
        raise
