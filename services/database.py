from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from core.config import settings
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Створюємо асинхронний двигун
engine = create_async_engine(
    str(settings.ASYNC_DATABASE_URL),
    echo=settings.DEBUG
)

async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    nickname = Column(String(settings.MAX_NICKNAME_LENGTH), nullable=False)
    email = Column(String, unique=True, nullable=False)
    game_id = Column(String, unique=True, nullable=False)
    is_registered = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

async def init_db():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("База даних успішно ініціалізована")
    except Exception as e:
        logger.error(f"Помилка при ініціалізації бази даних: {e}")
        raise

async def get_db():
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Помилка при роботі з базою даних: {e}")
            raise
        finally:
            await session.close()
