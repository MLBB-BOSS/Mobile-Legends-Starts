# utils/db.py

# -------------------------
# 📦 Імпорти
# -------------------------
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import logging

# Імпортуємо ваші моделі
from .models import User, Item  # Замініть на ваші реальні моделі

# -------------------------
# 📝 Конфігурація Логування
# -------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------------
# 🔗 Налаштування Бази Даних
# -------------------------
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@hostname/dbname")

# -------------------------
# 🛠️ Створення Асинхронного Engine
# -------------------------
async_engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Виводити SQL-запити в логи
    future=True
)

# -------------------------
# 🛠️ Створення Асинхронної Сесії
# -------------------------
async_session = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# -------------------------
# 🛠️ Базовий Клас для Моделей
# -------------------------
Base = declarative_base()

# -------------------------
# 🛠️ Ініціалізація Бази Даних
# -------------------------
async def init_db():
    """
    Ініціалізує базу даних, створюючи всі таблиці відповідно до моделей.
    """
    async with async_engine.begin() as conn:
        # Додаємо всі моделі до метаданих
        # Якщо у вас багато моделей, імпортуйте їх усюди
        await conn.run_sync(Base.metadata.create_all)
    logger.info("База даних ініціалізована успішно.")