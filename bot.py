import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage  # Рекомендовано замінити на RedisStorage2 для продуктивних ботів
from config import settings
from handlers import setup_handlers  # Імпорт функції реєстрації обробників
from utils.db import async_engine, async_session, init_db
from middlewares.database import DatabaseMiddleware
from sqlalchemy.ext.asyncio import AsyncEngine

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    logger.info("Starting bot initialization...")

    # Ініціалізація бота
    bot = Bot(
        token=settings.TELEGRAM_BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        session=AiohttpSession()
    )

    # Ініціалізація диспетчера з асинхронним сховищем
    from aiogram.fsm.storage.redis import RedisStorage2

    storage = RedisStorage2(
        host='localhost',  # Змініть на ваш хост Redis
        port=6379,         # Змініть на ваш порт Redis
        db=settings.REDIS_DB,
        password=settings.REDIS_PASSWORD if hasattr(settings, 'REDIS_PASSWORD') else None,
        timeout=1,
        connection_pool=None,
    )

    dp = Dispatcher(storage=storage)

    try:
        # Ініціалізація бази даних
        logger.info("Initializing database...")
        await init_db()

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