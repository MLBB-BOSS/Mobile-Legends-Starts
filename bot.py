import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from config import settings
from utils.db import engine, async_session, init_db
from models.base import Base
import models.user
import models.user_stats

from middlewares.database import DatabaseMiddleware
from handlers.base import setup_handlers
from handlers.missing_handlers import setup_missing_handlers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(
    token=settings.TELEGRAM_BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    session=AiohttpSession()
)

dp = Dispatcher(storage=MemoryStorage())

dp.message.middleware(DatabaseMiddleware(async_session))
dp.callback_query.middleware(DatabaseMiddleware(async_session))

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Tables created successfully.")

async def register_handlers():
    try:
        setup_handlers(dp)
        setup_missing_handlers(dp)
        logger.info("Handlers registered successfully.")
    except Exception as handler_error:
        logger.error(f"Handler setup error: {handler_error}")
        raise

async def shutdown():
    if bot.session:
        await bot.session.close()
    if engine:
        await engine.dispose()
    logger.info("Resources closed successfully.")

async def main():
    logger.info("Starting bot...")
    try:
        logger.info("Initializing database...")
        await init_db()
        await create_tables()
        await register_handlers()
        logger.info("Starting polling...")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Error while running bot: {e}")
    finally:
        await shutdown()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped!")
