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
from database import engine, DatabaseMiddleware, async_session  # Імпортуємо async_session
from models.base import Base
import models.user
import models.user_stats

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(
    token=settings.TELEGRAM_BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    session=AiohttpSession()
)
dp = Dispatcher(storage=MemoryStorage())

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Tables created successfully.")

async def main():
    logger.info("Starting bot...")
    try:
        await create_tables()

        # Замість get_db_session передаємо async_session напряму
        # async_session - це sessionmaker, при виклику async_session() отримуємо AsyncSession
        dp.message.middleware(DatabaseMiddleware(async_session))
        dp.callback_query.middleware(DatabaseMiddleware(async_session))

        setup_handlers(dp)
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