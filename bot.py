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
from handlers.navigation import router as navigation_router
from handlers.profile import router as profile_router
from handlers.heroes import router as heroes_router
from handlers.tournaments import router as tournaments_router
from handlers.guides import router as guides_router
from handlers.builds import router as builds_router
from handlers.teams import router as teams_router
from handlers.challenges import router as challenges_router
from handlers.bust import router as bust_router
from handlers.trading import router as trading_router
from handlers.start_intro import router as start_router
from handlers.main_menu import router as main_menu_router

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
            self._register_routers()
            logger.info("Dispatcher initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize dispatcher: {e}")
            raise

    def _register_routers(self) -> None:
        """Реєстрація всіх роутерів"""
        try:
            # Реєстрація роутерів в правильному порядку
            routers = [
                start_router,          # Роутер для команди /start та інтро
                main_menu_router,      # Роутер головного меню
                navigation_router,     # Роутер навігації
                profile_router,        # Роутер профілю
                heroes_router,         # Роутер героїв
                tournaments_router,    # Роутер турнірів
                guides_router,         # Роутер гайдів
                builds_router,         # Роутер білдів
                teams_router,          # Роутер команд
                challenges_router,     # Роутер челенджів
                bust_router,          # Роутер бусту
                trading_router,        # Роутер торгівлі
            ]

            for router in routers:
                self.dp.include_router(router)
                logger.info(f"Registered router: {router.__class__.__name__}")

            setup_handlers(self.dp)  # Додаткові хендлери, якщо такі є
            logger.info("All routers registered successfully")
        except Exception as e:
            logger.error(f"Failed to register routers: {e}")
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
