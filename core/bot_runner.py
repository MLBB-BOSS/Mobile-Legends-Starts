# core/bot_runner.py

import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.bot import DefaultBotProperties
import logging
import aiogram

# Встановлюємо рівень логування
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Перевірка версії aiogram
logger.info(f"aiogram version: {aiogram.__version__}")

# Спробуємо імпортувати Text окремо
try:
    from aiogram.filters import F Text
    logger.info("Успішно імпортовано Text з aiogram.filters")
except ImportError as e:
    logger.exception(f"Не вдалося імпортувати Text з aiogram.filters: {e}")
    raise

# Імпортуємо роутери
from handlers.start_command import router as start_router
from handlers.menu_handlers import router as menu_router
from handlers.message_handlers import router as message_router

API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not API_TOKEN:
    logger.critical("Не встановлено змінну середовища TELEGRAM_BOT_TOKEN")
    raise ValueError("Не встановлено змінну середовища TELEGRAM_BOT_TOKEN")

async def main():
    try:
        # Використовуємо DefaultBotProperties для встановлення parse_mode
        default_properties = DefaultBotProperties(parse_mode='HTML')
        bot = Bot(token=API_TOKEN, default=default_properties)
        storage = MemoryStorage()
        dp = Dispatcher(storage=storage)

        # Реєструємо роутери
        dp.include_router(start_router)
        dp.include_router(menu_router)
        dp.include_router(message_router)

        logger.info("Бот стартував.")
        await dp.start_polling(bot)
    except Exception as e:
        logger.exception(f"Помилка під час запуску бота: {e}")
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())
