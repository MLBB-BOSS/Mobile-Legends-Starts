# main_application.py

import os
import asyncio
import logging
from core.bot_runner import run_bot
from core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from services.init_services import init_services

from dotenv import load_dotenv

# Завантажуємо змінні середовища з .env файлу
load_dotenv()

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Отримуємо DATABASE_URL з Heroku або локального .env
database_url = os.getenv('DATABASE_URL')
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql+asyncpg://', 1)

# Створюємо engine для бази даних
engine = create_async_engine(
    database_url or settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10
)

# Створюємо фабрику сесій
AsyncSessionFactory = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def notify_user(message: str):
    """
    Callback-функція для відправки повідомлень користувачам через бот.

    Args:
        message (str): Повідомлення для відправки.
    """
    # Локальний імпорт, щоб уникнути циклічного імпорту
    from core.bot import bot  # Використовуйте локальний імпорт, щоб уникнути циклу

    # Наприклад, відправити повідомлення адміністратору
    admin_id = os.getenv('ADMIN_USER_ID')
    if admin_id:
        try:
            await bot.send_message(chat_id=admin_id, text=message)
            logger.info(f"Sent notification to admin: {message}")
        except Exception as e:
            logger.error(f"Failed to send notification to admin: {e}")

async def init_db():
    """Ініціалізація бази даних"""
    try:
        async with engine.begin() as conn:
            # При необхідності створюйте всі таблиці
            from models import Base  # Переконайтесь, що ви імпортуєте Base
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database connection established successfully")
    except Exception as e:
        logger.error(f"Error connecting to database: {e}", exc_info=True)
        raise

async def main():
    """Головна функція запуску"""
    try:
        # Ініціалізуємо базу даних
        await init_db()

        # Ініціалізуємо сервіси з передачею callback-функції
        services = await init_services(notify_callback=notify_user)

        # Запускаємо бота
        await run_bot(AsyncSessionFactory)

    except Exception as e:
        logger.error(f"Error during startup: {e}", exc_info=True)
        raise
    finally:
        # Закриваємо з'єднання з базою даних
        await engine.dispose()

if __name__ == "__main__":
    try:
        # Встановлюємо правильний часовий пояс
        os.environ['TZ'] = 'UTC'
        import time
        time.tzset()

        # Запускаємо головну функцію
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
