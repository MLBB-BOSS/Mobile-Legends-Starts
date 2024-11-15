from typing import Optional, AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, Boolean, DateTime, text
import logging
from datetime import datetime

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

# Створюємо базовий клас для моделей
Base = declarative_base()

# Створюємо підключення до бази даних
DATABASE_URL = "postgresql+asyncpg://udoepvnsfd1v4p:p06d554a757b594fc448b0fe17f59b24af6e1ed553f9cd262a36d4e56fd87a37f@c9tiftt16dc3eo.cluster-czz5s0kz4scl.eu-west-1.rds.amazonaws.com:5432/d76pc5iknkd84"

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30
)

# Створюємо фабрику сесій
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Базова модель користувача
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, telegram_id={self.telegram_id})>"

async def init_db():
    """Ініціалізація бази даних"""
    try:
        async with engine.begin() as conn:
            # Перевіряємо підключення
            await conn.execute(text("SELECT 1"))
            logger.info("Підключення до бази даних встановлено")

            # Перевіряємо існування таблиць
            check_query = text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'users'
                )
            """)
            result = await conn.execute(check_query)
            exists = await result.scalar()

            if not exists:
                logger.info("Створюємо таблиці...")
                await conn.run_sync(Base.metadata.create_all)
                logger.info("Таблиці успішно створені")
            else:
                logger.info("Таблиці вже існують")

        return True

    except Exception as e:
        logger.error(f"Помилка при ініціалізації бази даних: {str(e)}")
        return False

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Отримання сесії бази даних"""
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Помилка сесії бази даних: {e}")
            raise
        finally:
            await session.close()
