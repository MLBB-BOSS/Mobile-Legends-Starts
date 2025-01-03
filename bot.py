import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import settings  # Імпорт з кореневої директорії
from utils.db import init_db, check_connection
from handlers.base import router as base_router
from handlers.profile import profile_router
from utils.charts import charts_router
from handlers.navigation import router as navigation_router
from handlers.missing_handlers import router as missing_handlers_router
from handlers.callbacks import router as callbacks_router

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levellevel)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Ініціалізація бота та диспетчера
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# Реєстрація роутерів
dp.include_router(base_router)
dp.include_router(profile_router)
dp.include_router(charts_router)
dp.include_router(navigation_router)
dp.include_router(missing_handlers_router)
dp.include_router(callbacks_router)

async def main():
    try:
        logger.info(f"Starting {settings.APP_NAME} at {settings.CURRENT_TIME}")
        logger.info(f"Initialized by {settings.CURRENT_USER}")
        
        # Перевірка з'єднання з базою даних
        if not await check_connection():
            logger.error("Failed to connect to database")
            return

        # Ініціалізація бази даних
        await init_db()
        
        # Запуск бота
        logger.info("Bot is running...")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Startup error: {e}")
    finally:
        logger.info("Shutting down...")
        await bot.session.close()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Critical error: {e}")