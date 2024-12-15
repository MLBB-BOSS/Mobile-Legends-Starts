import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from config import settings
from handlers import router
from utils.db import engine, AsyncSessionLocal, DatabaseMiddleware, Base

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_tables():
    """Створює таблиці у базі даних, якщо вони ще не існують."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Tables created successfully.")

async def main():
    """Основна функція для запуску бота."""
    logger.info("Starting bot...")

    # Ініціалізація бота
    bot = Bot(
        token=settings.TELEGRAM_BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        session=AiohttpSession()  # Використання сесії Aiohttp
    )

    # Ініціалізація диспетчера
    dp = Dispatcher(storage=MemoryStorage())

    # Створення таблиць у базі даних
    await create_tables()

    # Додавання DatabaseMiddleware
    dp.message.middleware(DatabaseMiddleware(AsyncSessionLocal))
    dp.callback_query.middleware(DatabaseMiddleware(AsyncSessionLocal))
    dp.inline_query.middleware(DatabaseMiddleware(AsyncSessionLocal))

    # Підключення хендлерів
    dp.include_router(router)

    try:
        # Запуск полінгу
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Error while running bot: {e}")
    finally:
        # Закриття сесії бота
        await bot.session.close()
        logger.info("Bot session closed.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped!")