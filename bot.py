import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from config import settings
from handlers import setup_handlers  # Змінено імпорт
from utils.db import engine, async_session, init_db
from models.base import Base
import models.user
import models.user_stats
from middlewares.database import DatabaseMiddleware

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def create_tables():
    """Створює таблиці у базі даних"""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
        raise

async def main():
    logger.info("Starting bot initialization...")
    
    # Ініціалізація бота
    bot = Bot(
        token=settings.TELEGRAM_BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        session=AiohttpSession()
    )
    
    # Ініціалізація диспетчера
    dp = Dispatcher(storage=MemoryStorage())
    
    try:
        # Ініціалізація бази даних
        logger.info("Initializing database...")
        await init_db()
        await create_tables()
        
        # Додавання middleware
        dp.message.middleware(DatabaseMiddleware(async_session))
        dp.callback_query.middleware(DatabaseMiddleware(async_session))
        
        # Налаштування обробників
        logger.info("Setting up handlers...")
        setup_handlers(dp)
        
        # Запуск бота
        logger.info("Starting polling...")
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"Critical error: {e}")
        raise
    finally:
        if bot.session:
            await bot.session.close()
            logger.info("Bot session closed")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped!")
    except Exception as e:
        logger.critical(f"Unexpected error: {e}")
