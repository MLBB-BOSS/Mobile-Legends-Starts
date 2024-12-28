import asyncio
import logging
from typing import Optional
from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy.exc import SQLAlchemyError

from config import settings
from handlers.base import setup_handlers
from utils.db import engine, async_session, init_db
from models.base import Base
import models.user
import models.user_stats
from middlewares.database import DatabaseMiddleware

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('bot.log')
    ]
)
logger = logging.getLogger(__name__)

class MLBBBot:
    def __init__(self):
        """Ініціалізація бота та його компонентів"""
        self.bot: Optional[Bot] = None
        self.dp: Optional[Dispatcher] = None
        self._setup_bot()
        self._setup_dispatcher()

    def _setup_bot(self) -> None:
        """Налаштування бота"""
        try:
            session = AiohttpSession()
            self.bot = Bot(
                token=settings.TELEGRAM_BOT_TOKEN,
                default=DefaultBotProperties(parse_mode=ParseMode.HTML),
                session=session
            )
            logger.info("Bot initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize bot: {e}")
            raise

    def _setup_dispatcher(self) -> None:
        """Налаштування диспетчера"""
        try:
            self.dp = Dispatcher(storage=MemoryStorage())
            self._setup_middlewares()
            setup_handlers(self.dp)
            logger.info("Dispatcher initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize dispatcher: {e}")
            raise

    def _setup_middlewares(self) -> None:
        """Налаштування middleware"""
        try:
            self.dp.message.middleware(DatabaseMiddleware(async_session))
            self.dp.callback_query.middleware(DatabaseMiddleware(async_session))
            logger.info("Middlewares set up successfully")
        except Exception as e:
            logger.error(f"Failed to set up middlewares: {e}")
            raise

    @asynccontextmanager
    async def bot_context(self):
        """Контекстний менеджер для роботи з ботом"""
        try:
            yield
        finally:
            if self.bot and self.bot.session:
                await self.bot.session.close()
                logger.info("Bot session closed")

    async def create_tables(self) -> None:
        """Створення таблиць в базі даних"""
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables created successfully")
        except SQLAlchemyError as e:
            logger.error(f"Failed to create database tables: {e}")
            raise

    async def start(self) -> None:
        """Запуск бота"""
        try:
            logger.info("Starting bot...")
            await init_db()
            await self.create_tables()
            await self.dp.start_polling(self.bot)
        except Exception as e:
            logger.error(f"Error while running bot: {e}")
            raise

async def main():
    """Головна функція запуску бота"""
    bot_instance = MLBBBot()
    async with bot_instance.bot_context():
        try:
            await bot_instance.start()
        except Exception as e:
            logger.critical(f"Critical error occurred: {e}")
            return 1
    return 0

if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        if exit_code:
            logger.warning(f"Bot stopped with exit code: {exit_code}")
        else:
            logger.info("Bot stopped successfully!")
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped by user!")
    except Exception as e:
        logger.critical(f"Unexpected error occurred: {e}")
        exit(1)
