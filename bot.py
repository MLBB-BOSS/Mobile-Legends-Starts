import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties  # Додано імпорт
from aiogram.fsm.storage.memory import MemoryStorage  # Заміна на RedisStorage для масштабованості
from config import settings
from utils.db import engine, async_session, init_db
from models.base import Base
import models.user
import models.user_stats
from middlewares.database import DatabaseMiddleware
from handlers import setup_handlers  # Імпортуємо з handlers/__init__.py
from rich.logging import RichHandler
from rich.console import Console

# Логування з Rich
console = Console()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[RichHandler(console=console)],
)

logger = logging.getLogger("rich")

# Ініціалізація бота
bot = Bot(
    token=settings.TELEGRAM_BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),  # Використовується DefaultBotProperties
    session=AiohttpSession(),
)

# Заміна на RedisStorage для масштабованості
storage = MemoryStorage()  # Для продакшн середовища RedisStorage
dp = Dispatcher(storage=storage)

# Реєстрація мідлвар
dp.message.middleware(DatabaseMiddleware(async_session))
dp.callback_query.middleware(DatabaseMiddleware(async_session))

async def create_tables():
    """Створення таблиць у базі даних."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Tables created successfully.")

async def register_handlers():
    """Реєстрація обробників."""
    try:
        setup_handlers(dp)
        logger.info("Handlers registered successfully.")
    except Exception as handler_error:
        logger.error(f"Handler setup error: {handler_error}")
        raise

async def shutdown():
    """Закриття ресурсів під час зупинки бота."""
    if bot.session:
        await bot.session.close()
    if engine:
        await engine.dispose()
    logger.info("Resources closed successfully.")

async def main():
    """Основна функція запуску бота."""
    logger.info("Starting bot...")
    try:
        logger.info("Initializing database...")
        await init_db()
        await create_tables()
        await register_handlers()
        logger.info("Starting polling...")
        async with bot:
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
