# bot.py
# UTC:22:20
# 2024-11-25
# Author: MLBB-BOSS
# Description: Main bot file
# The era of artificial intelligence.

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import settings
from database import init_db, reset_db, DatabaseMiddleware, async_session
from handlers import (
    main_menu_router,
    navigation_router,
    profile_router,
    mp3_player_router  # Додано новий обробник для MP3 плеєра
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def register_routers(dp: Dispatcher):
    """Реєстрація всіх роутерів"""
    logger.info("Registering routers...")
    
    # Основні роутери
    routers = [
        main_menu_router,
        navigation_router,
        profile_router,
        mp3_player_router  # Реєстрація нового обробника для MP3 плеєра
    ]
    
    for router in routers:
        dp.include_router(router)
        logger.info(f"Router {router.__class__.__name__} registered")
    
    logger.info("All routers registered successfully")

async def main():
    # Log startup info
    logger.info("Starting bot initialization...")
    
    try:
        if not settings.BOT_TOKEN:
            raise ValueError("No bot token provided. Please set TELEGRAM_BOT_TOKEN environment variable.")
        
        # Updated Bot initialization for aiogram 3.7.0
        bot = Bot(
            token=settings.BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        dp = Dispatcher()
        
        # Register middlewares
        dp.update.middleware(DatabaseMiddleware(async_session))
        
        # Register all routers
        await register_routers(dp)
        
        # Reset and Initialize database
        logger.info("Resetting database...")
        await reset_db()
        logger.info("Database reset successfully")
        
        logger.info("Initializing database...")
        await init_db()
        logger.info("Database initialized successfully")
        
        # Start polling in an infinite loop
        logger.info("Starting bot polling...")
        while True:
            try:
                await dp.start_polling(bot)
            except Exception as polling_error:
                logger.error(f"Polling error: {polling_error}", exc_info=True)
                logger.info("Waiting 5 seconds before retry...")
                await asyncio.sleep(5)
                
    except Exception as e:
        logger.error(f"Critical error during startup: {e}", exc_info=True)
        raise
    finally:
        logger.info("Shutting down...")
        if 'bot' in locals():
            await bot.session.close()

if __name__ == "__main__":
    try:
        # Create event loop
        loop = asyncio.get_event_loop()
        # Run the main function forever
        loop.run_until_complete(main())
        loop.run_forever()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot stopped due to error: {e}", exc_info=True)
    finally:
        # Properly close the event loop
        if 'loop' in locals():
            loop.close()
