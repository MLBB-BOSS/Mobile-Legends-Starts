# UTC:22:00
# 2024-11-25
# bot.py
# Author: MLBB-BOSS
# Description: Main bot initialization and dispatcher setup
# The era of artificial intelligence.

import asyncio
import logging
import sys
from contextlib import AsyncExitStack

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.bot import DefaultBotProperties

from config import settings
from database import init_db, close_db, async_session  # Переконайтеся, що async_session експортується
from middlewares.database import DatabaseMiddleware  # Імпорт Middleware
from handlers import main_menu_router, navigation_router, profile_handlers_router  # Видалено user_handlers_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

async def main():
    # Initialize resources using AsyncExitStack for proper cleanup
    async with AsyncExitStack() as stack:
        try:
            # Initialize database
            await init_db()
            stack.push_async_callback(close_db)

            # Initialize bot and dispatcher
            bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
            stack.push_async_callback(bot.session.close)

            # Setup dispatcher with storage
            dp = Dispatcher(storage=MemoryStorage())

            # Register middlewares
            dp.message.middleware(DatabaseMiddleware(async_session))  # Реєстрація Middleware для повідомлень

            # Register routers
            dp.include_router(main_menu_router)
            dp.include_router(navigation_router)
            dp.include_router(profile_handlers_router)  # Додано профільні хендлери

            # Start polling
            logger.info("Starting Mobile Legends Tournament Bot...")
            await dp.start_polling(
                bot,
                allowed_updates=dp.resolve_used_update_types()
            )

        except Exception as e:
            logger.error(f"Critical error: {e}", exc_info=True)
            sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
    except Exception as e:
        logger.critical(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)
