# File: core/bot_runner.py

import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers import main_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode="HTML")
    # Dispatcher is a root router
    dp = Dispatcher()
    
    # Include main router
    dp.include_router(main_router)
    
    # Delete webhook before polling
    await bot.delete_webhook(drop_pending_updates=True)
    
    try:
        logger.info("Starting bot polling...")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped!")
