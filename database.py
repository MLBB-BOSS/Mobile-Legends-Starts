import logging
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from config import settings

# Configure logging
logger = logging.getLogger(__name__)

# Create async engine
engine = create_async_engine(
    settings.db_url,
    echo=settings.DEBUG,
    pool_size=20,
    pool_pre_ping=True,
    pool_recycle=300
)

# Create session factory
AsyncSessionFactory = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Database session generator"""
    session = AsyncSessionFactory()
    try:
        yield session
    except SQLAlchemyError as e:
        logger.error(f"Database error: {str(e)}")
        await session.rollback()
        raise
    finally:
        await session.close()

async def init_db() -> None:
    """Initialize database tables"""
    from models.base import Base
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database initialized successfully")
    except SQLAlchemyError as e:
        logger.error(f"Database initialization error: {str(e)}")
        raise

async def reset_db() -> None:
    """Reset (drop and recreate) the database"""
    from models.base import Base
    try:
        async with engine.begin() as conn:
            # Drop all existing tables
            logger.warning("Dropping all tables...")
            await conn.run_sync(Base.metadata.drop_all)
            logger.info("All tables dropped successfully.")

            # Recreate tables
            logger.info("Recreating tables...")
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Database reset and tables recreated successfully.")
    except SQLAlchemyError as e:
        logger.error(f"Database reset error: {str(e)}")
        raise

async def close_db() -> None:
    """Close database connections"""
    try:
        await engine.dispose()
        logger.info("Database connections closed")
    except SQLAlchemyError as e:
        logger.error(f"Error closing database: {str(e)}")
        raise
