# UTC:22:02
# 2024-11-24
# bot.py
# Author: MLBB-BOSS
# Description: Main bot initialization and configuration
# The era of artificial intelligence.

import asyncio
import logging
import sys
import os
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

# Import routers
from handlers import main_menu_router, navigation_router, user_handlers_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# Bot token from environment
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    logger.error("No TELEGRAM_BOT_TOKEN provided!")
    sys.exit(1)

async def main():
    # Initialize bot and dispatcher
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    
    # Register routers
    dp.include_router(main_menu_router)
    dp.include_router(navigation_router)
    dp.include_router(user_handlers_router)
    
    try:
        logger.info("Starting bot...")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Critical error: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
