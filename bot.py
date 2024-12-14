# bot.py
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage  # Розгляньте використання RedisStorage для продакшну
from config import settings
from handlers.base import setup_handlers
from database import engine, DatabaseMiddleware, async_session
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
dp = Dispatcher(storage=MemoryStorage())  # Розгляньте використання RedisStorage для продакшну

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Таблиці створено успішно.")

async def main():
    logger.info("Запуск бота...")
    try:
        await create_tables()

        # Додаємо DatabaseMiddleware
        dp.message.middleware(DatabaseMiddleware(async_session))
        dp.callback_query.middleware(DatabaseMiddleware(async_session))

        setup_handlers(dp)
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Помилка під час запуску бота: {e}")
    finally:
        if bot.session:
            await bot.session.close()
        await engine.dispose()  # Закриваємо з'єднання з базою даних

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот зупинено!")