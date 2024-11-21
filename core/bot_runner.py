# core/bot_runner.py
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

# Отримуємо токен з змінних середовища
API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not API_TOKEN:
    logger.critical("Не встановлено змінну середовища TELEGRAM_BOT_TOKEN")
    raise ValueError("Не встановлено змінну середовища TELEGRAM_BOT_TOKEN")

async def main():
    try:
        # Створюємо об'єкт бота
        bot = Bot(
            token=API_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        
        # Ініціалізуємо сховище та диспетчер
        storage = MemoryStorage()
        dp = Dispatcher(storage=storage)

        # Реєструємо всі роутери
        routers = [
            start_router,
            menu_router,
            message_router,
            error_router,
            hero_class_router,
            hero_router,
            navigation_router
        ]

        for router in routers:
            dp.include_router(router)

        logger.info("Бот стартував.")
        
        # Запускаємо поллінг
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.exception(f"Помилка під час запуску бота: {e}")
        raise
        
    finally:
        if 'bot' in locals():
            await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())
