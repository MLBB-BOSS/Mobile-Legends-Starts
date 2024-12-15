# bot.py

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession  # Виправлено
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage  # Для FSM
from config import settings
from handlers.base import setup_handlers
from utils.db import engine, AsyncSessionLocal, DatabaseMiddleware, Base
import models.user  # Імпортуємо модель User
import models.user_stats  # Імпортуємо модель UserStats

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config import settings

# Створення асинхронного двигуна
engine = create_async_engine(
    settings.db_url,
    echo=settings.DEBUG,
    pool_size=10,
    max_overflow=20
)

# Фабрика асинхронних сесій
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ініціалізація бота
bot = Bot(
    token=settings.TELEGRAM_BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    session=AiohttpSession()  # Явне визначення сесії
)

# Ініціалізація диспетчера з підтримкою FSM
dp = Dispatcher(storage=MemoryStorage())  # Додано storage для FSM

async def create_tables():
    """Створює таблиці у базі даних, якщо вони ще не існують."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Tables created successfully.")

async def main():
    logger.info("Starting bot...")
    try:
        # Створення таблиць перед запуском бота
        await create_tables()

        # Додавання DatabaseMiddleware до Dispatcher
        dp.message.middleware(DatabaseMiddleware(AsyncSessionLocal))
        dp.callback_query.middleware(DatabaseMiddleware(AsyncSessionLocal))
        dp.inline_query.middleware(DatabaseMiddleware(AsyncSessionLocal))
        # Додайте інші типи оновлень за потребою

        # Налаштування хендлерів
        setup_handlers(dp)

        # Запуск полінгу
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Error while running bot: {e}")
    finally:
        if bot.session:
            await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped!")