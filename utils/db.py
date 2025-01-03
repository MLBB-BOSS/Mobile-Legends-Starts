from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
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
