import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
import logging
import aiogram

# Встановлюємо рівень логування
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Перевірка версії aiogram
logger.info(f"aiogram version: {aiogram.__version__}")

# Імпортуємо роутери
from handlers.start_command import router as start_router
from handlers.menu_handlers import router as menu_router
from handlers.message_handlers import router as message_router
from handlers.error_handler import router as error_router
from handlers.hero_class_handlers import router as hero_class_router
from handlers.hero_handlers import router as hero_router
from handlers.navigation_handlers import router as navigation_router

API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not API_TOKEN:
    logger.critical("Не встановлено змінну середовища TELEGRAM_BOT_TOKEN")
    raise ValueError("Не встановлено змінну середовища TELEGRAM_BOT_TOKEN")

async def main():
    try:
        # Створюємо об'єкт бота з новим синтаксисом для parse_mode
        bot = Bot(
            token=API_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        storage = MemoryStorage()
        dp = Dispatcher(storage=storage)

        # Реєструємо роутери
        dp.include_router(start_router)
        dp.include_router(menu_router)
        dp.include_router(message_router)
        dp.include_router(error_router)
        dp.include_router(hero_class_router)
        dp.include_router(hero_router)
        dp.include_router(navigation_router)

        logger.info("Бот стартував.")
        await dp.start_polling(bot)
    except Exception as e:
        logger.exception(f"Помилка під час запуску бота: {e}")
        raise  # Re-raise the exception to ensure proper cleanup
    finally:
        if 'bot' in locals():  # Check if bot was created before trying to close session
            await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())
