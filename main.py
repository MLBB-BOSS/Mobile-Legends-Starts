import os
import asyncio
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler
from core.bot import run_bot
from core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from services.base_service import BaseService
from typing import Any

# Створення директорії для логів, якщо її ще немає
LOG_DIR: str = 'logs'
LOG_FILE: str = os.path.join(LOG_DIR, 'app.log')

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Налаштування логування
logger: logging.Logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter: logging.Formatter = logging.Formatter(
    '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Обробник для консолі
console_handler: logging.StreamHandler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Обробник для файлу з ротацією
file_handler: RotatingFileHandler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=5 * 1024 * 1024,  # 5 МБ
    backupCount=5
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Отримуємо DATABASE_URL з змінних середовища або конфігурації
database_url: str = os.getenv('DATABASE_URL', settings.DATABASE_URL)
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql+asyncpg://', 1)

# Створюємо engine для бази даних
engine: Any = create_async_engine(
    database_url,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10
)

# Створюємо фабрику сесій
AsyncSessionFactory: sessionmaker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db() -> None:
    """Ініціалізація бази даних"""
    try:
        async with engine.begin() as conn:
            # При необхідності створюйте всі таблиці
            # Наприклад, якщо використовуєте SQLAlchemy ORM:
            # from models import Base
            # await conn.run_sync(Base.metadata.create_all)
            logger.info("✅ Підключення до бази даних успішно встановлено")
    except Exception as e:
        logger.error(f"❌ Помилка підключення до бази даних: {e}", exc_info=True)
        raise

async def startup() -> None:
    """Функція ініціалізації при запуску"""
    try:
        logger.info(f"🚀 Запуск MLBB-BOSS бота о {datetime.utcnow()} UTC")
        logger.info(f"🔧 Режим відладки: {settings.DEBUG}")

        # Ініціалізуємо базу даних
        await init_db()

        # Ініціалізуємо сервіси
        service: BaseService = BaseService()
        service.perform_action()

        # Запускаємо бота
        await run_bot(AsyncSessionFactory)

    except Exception as e:
        logger.error(f"❌ Помилка під час запуску: {e}", exc_info=True)
        await shutdown()
        raise

async def shutdown() -> None:
    """Функція очищення при зупинці"""
    try:
        logger.info("🔄 Завершення роботи...")

        # Закриваємо з'єднання з базою даних
        await engine.dispose()
        logger.info("✅ З'єднання з базою даних закрито")
    except Exception as e:
        logger.error(f"❌ Помилка під час завершення роботи: {e}", exc_info=True)
        raise

def set_utc_timezone() -> None:
    """Встановлює UTC часовий пояс"""
    os.environ['TZ'] = 'UTC'
    try:
        import time
        time.tzset()
    except AttributeError:
        # time.tzset() не підтримується на Windows
        pass

if __name__ == "__main__":
    try:
        # Встановлюємо UTC часовий пояс
        set_utc_timezone()

        # Запускаємо бота
        asyncio.run(startup())

    except KeyboardInterrupt:
        logger.info("👋 Бот зупинено користувачем")
        asyncio.run(shutdown())

    except Exception as e:
        logger.error(f"❌ Несподівана помилка: {e}", exc_info=True)
        asyncio.run(shutdown())
