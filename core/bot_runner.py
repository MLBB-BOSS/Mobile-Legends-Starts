import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
import logging
import aiogram

# Set logging level
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Check aiogram version
logger.info(f"aiogram version: {aiogram.__version__}")

# Import routers
from handlers.start_command import router as start_router
from handlers.menu_handlers import router as menu_router
from handlers.message_handlers import router as message_router

API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not API_TOKEN:
    logger.critical("Environment variable TELEGRAM_BOT_TOKEN is not set")
    raise ValueError("Environment variable TELEGRAM_BOT_TOKEN is not set")

async def main():
    try:
        # Create bot object
        bot = Bot(token=API_TOKEN, parse_mode='HTML')
        storage = MemoryStorage()
        dp = Dispatcher(storage=storage)

        # Register routers
        dp.include_router(start_router)
        dp.include_router(menu_router)
        dp.include_router(message_router)

        logger.info("Bot started.")
        await dp.start_polling(bot)
    except Exception as e:
        logger.exception(f"Error while running the bot: {e}")
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())
