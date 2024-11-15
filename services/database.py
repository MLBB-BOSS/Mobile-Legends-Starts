from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, Boolean, DateTime
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

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    nickname = Column(String(32), nullable=False)
    email = Column(String, unique=True, nullable=False)
    game_id = Column(String, unique=True, nullable=False)
    is_registered = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<User(id={self.id}, nickname={self.nickname}, telegram_id={self.telegram_id})>"

# Створюємо підключення до бази даних
engine = create_async_engine(
    "postgresql+asyncpg://u19gdelo8pjkrg:pb95edc1e9dc17f2d21f8f49fe9e9c6a3c2eab4969e95adbfc2c69a5c753b9fdb@ccaml3dimis7eh.cluster-czz5s0kz4scl.eu-west-1.rds.amazonaws.com:5432/da4c4gk6ldknbt",
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

# Функція для ініціалізації бази даних
async def init_db():
    try:
        async with engine.begin() as conn:
            # Видаляємо стару таблицю, якщо вона існує
            await conn.run_sync(Base.metadata.drop_all)
            # Створюємо нові таблиці
            await conn.run_sync(Base.metadata.create_all)
            logger.info("База даних успішно ініціалізована")
    except Exception as e:
        logger.error(f"Помилка при ініціалізації бази даних: {e}")
        raise

# Функція для отримання сесії бази даних
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

# Допоміжні функції для роботи з користувачами
async def get_user_by_telegram_id(telegram_id: int) -> User | None:
    try:
        async with async_session() as session:
            from sqlalchemy import select
            result = await session.execute(
                select(User).where(User.telegram_id == telegram_id)
            )
            return result.scalar_one_or_none()
    except Exception as e:
        logger.error(f"Помилка при отриманні користувача: {e}")
        return None

async def create_user(
    telegram_id: int,
    nickname: str,
    email: str,
    game_id: str
) -> User | None:
    try:
        async with async_session() as session:
            user = User(
                telegram_id=telegram_id,
                nickname=nickname,
                email=email,
                game_id=game_id,
                is_registered=True
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user
    except Exception as e:
        logger.error(f"Помилка при створенні користувача: {e}")
        return None

async def update_user(user: User) -> bool:
    try:
        async with async_session() as session:
            session.add(user)
            await session.commit()
            return True
    except Exception as e:
        logger.error(f"Помилка при оновленні користувача: {e}")
        return False
