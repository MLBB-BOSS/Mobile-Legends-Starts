import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from config import settings
from handlers.base import setup_handlers
from handlers.missing_handlers import setup_missing_handlers
from utils.db import engine, async_session, init_db
from models.base import Base
import models.user
import models.user_stats

# Імпорт Middleware
from middlewares.database import DatabaseMiddleware  

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

# Додавання Middleware
dp.message.middleware(DatabaseMiddleware(async_session))
dp.callback_query.middleware(DatabaseMiddleware(async_session))

async def create_tables():
    """Створює таблиці у базі даних, якщо вони ще не існують."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Tables created successfully.")

async def register_handlers():
    """Реєстрація всіх хендлерів."""
    try:
        setup_handlers(dp)
        setup_missing_handlers(dp)
        logger.info("Handlers registered successfully.")
    except Exception as handler_error:
        logger.error(f"Handler setup error: {handler_error}")
        raise

async def shutdown():
    """Закриває ресурси перед завершенням роботи."""
    if bot.session:
        await bot.session.close()
    if engine:
        await engine.dispose()
    logger.info("Resources closed successfully.")

async def main():
    logger.info("Starting bot...")
    try:
        # Ініціалізація бази даних
        logger.info("Initializing database...")
        await init_db()

        # Створення таблиць перед запуском бота
        await create_tables()

        # Налаштування хендлерів
        await register_handlers()

        # Запуск полінгу
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