import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from core.config import settings
from services.database import init_models
from handlers import router

# Configure logging
logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Register routers
dp.include_router(router)

async def main():
    logger.info("Starting bot...")
    
    # Initialize database
    try:
        await init_models()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        return
    
    # Start polling
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Bot polling error: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
