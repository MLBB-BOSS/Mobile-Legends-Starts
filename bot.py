import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from config import settings
from database import init_db, DatabaseMiddleware, async_session
from handlers import main_menu, navigation, user_handlers

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    # Log startup info
    logger.info("Starting bot initialization...")
    
    # Initialize bot and dispatcher with error logging
    try:
        if not settings.BOT_TOKEN:
            raise ValueError("No bot token provided. Please set TELEGRAM_BOT_TOKEN environment variable.")
        
        bot = Bot(token=settings.BOT_TOKEN, parse_mode=ParseMode.HTML)
        dp = Dispatcher()
        
        # Register middlewares
        dp.update.middleware(DatabaseMiddleware(async_session))
        
        # Register all handlers
        dp.include_router(main_menu.router)
        dp.include_router(navigation.router)
        dp.include_router(user_handlers.router)
        
        # Initialize database
        logger.info("Initializing database...")
        await init_db()
        logger.info("Database initialized successfully")
        
        # Start polling
        logger.info("Starting bot polling...")
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"Critical error during startup: {e}", exc_info=True)
        raise
    finally:
        logger.info("Shutting down...")
        if 'bot' in locals():
            await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot stopped due to error: {e}", exc_info=True)
