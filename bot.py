# bot.py
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from config import settings
from handlers.base import setup_handlers
from database import engine, DatabaseMiddleware
from models.base import Base
import models.user
import models.user_stats
from utils.db import get_db_session

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ініціалізація бота
bot = Bot(
    token=settings.TELEGRAM_BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    session=AiohttpSession()
)

# Ініціалізація диспетчера з підтримкою FSM
dp = Dispatcher(storage=MemoryStorage())

async def create_tables():
    """Створює таблиці у базі даних, якщо вони ще не існують."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Tables created successfully.")

async def main():
    logger.info("Starting bot...")
    try:
        # Створення таблиць перед запуском бота
        await create_tables()

        # Реєстрація мідлвару для керування сесіями БД
        dp.message.middleware(DatabaseMiddleware(get_db_session))
        dp.callback_query.middleware(DatabaseMiddleware(get_db_session))

        # Налаштування хендлерів
        setup_handlers(dp)

        # Запуск полінгу
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Error while running bot: {e}")
    finally:
        if bot.session:
            await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped!")