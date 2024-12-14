# bot.py
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage  # Розгляньте використання RedisStorage для продакшну
from config import settings
from handlers.base import setup_handlers
from database import engine, DatabaseMiddleware, async_session
from models import Base  # Імпортуємо базу даних та всі моделі через models/__init__.py

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ініціалізація бота
bot = Bot(
    token=settings.TELEGRAM_BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    session=AiohttpSession()
)

# Ініціалізація диспетчера з MemoryStorage (замість цього використовуйте RedisStorage для продакшну)
dp = Dispatcher(storage=MemoryStorage())

async def create_tables():
    logger.info("Створення таблиць...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Таблиці створено успішно.")

async def main():
    logger.info("Запуск бота...")
    try:
        await create_tables()
        logger.info("Таблиці створено успішно.")
        
        # Додаємо DatabaseMiddleware
        dp.message.middleware(DatabaseMiddleware(async_session))
        dp.callback_query.middleware(DatabaseMiddleware(async_session))
        logger.info("DatabaseMiddleware додано.")
        
        # Налаштовуємо обробники
        setup_handlers(dp)
        logger.info("Handlers встановлено.")
        
        # Запуск Polling
        logger.info("Початок Polling...")
        await dp.start_polling(bot)
        logger.info("Polling завершено.")
    except Exception as e:
        logger.error(f"Помилка під час запуску бота: {e}")
    finally:
        if bot.session:
            await bot.session.close()
            logger.info("Bot session закрита.")
        await engine.dispose()  # Закриваємо з'єднання з базою даних
        logger.info("З'єднання з базою даних закрито.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот зупинено!")