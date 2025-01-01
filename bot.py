# bot.py
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
from handlers import setup_handlers
from utils.db import engine, async_session, init_db
from utils.message_utils import MessageManager
from models.base import Base
import models.user
import models.user_stats
from middlewares.database import DatabaseMiddleware

# Logging setup
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
    """Main bot class"""
    
    def __init__(self):
        """Initialize bot and its components"""
        self.bot: Optional[Bot] = None
        self.dp: Optional[Dispatcher] = None
        self.message_manager: Optional[MessageManager] = None
        self._setup_bot()
        self._setup_dispatcher()

    def _setup_bot(self) -> None:
        """Setup bot instance"""
        try:
            session = AiohttpSession()
            self.bot = Bot(
                token=settings.TELEGRAM_BOT_TOKEN,
                default=DefaultBotProperties(parse_mode=ParseMode.HTML),
                session=session
            )
            # Initialize message manager
            self.message_manager = MessageManager(self.bot)
            logger.info("Bot initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize bot: {e}")
            raise

    def _setup_dispatcher(self) -> None:
        """Setup dispatcher and register handlers"""
        try:
            self.dp = Dispatcher(storage=MemoryStorage())
            self._setup_middlewares()
            
            # Register all handlers
            setup_handlers(self.dp, self.message_manager)
            
            logger.info("Dispatcher initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize dispatcher: {e}")
            raise

    def _setup_middlewares(self) -> None:
        """Setup middlewares"""
        try:
            # Database middleware
            self.dp.message.middleware(DatabaseMiddleware(async_session))
            self.dp.callback_query.middleware(DatabaseMiddleware(async_session))
            
            # Add other middlewares here
            
            logger.info("Middlewares set up successfully")
        except Exception as e:
            logger.error(f"Failed to set up middlewares: {e}")
            raise

    @asynccontextmanager
    async def bot_context(self):
        """Context manager for bot lifecycle"""
        try:
            yield
        finally:
            if self.bot and self.bot.session:
                await self.bot.session.close()
                logger.info("Bot session closed")

    async def create_tables(self) -> None:
        """Create database tables"""
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables created successfully")
        except SQLAlchemyError as e:
            logger.error(f"Failed to create database tables: {e}")
            raise

    async def _setup_database(self) -> None:
        """Setup database"""
        try:
            await init_db()
            await self.create_tables()
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise

    async def start(self) -> None:
        """Start bot"""
        try:
            logger.info("Starting bot...")
            
            # Initialize database
            await self._setup_database()
            
            # Start polling
            await self.dp.start_polling(
                self.bot,
                allowed_updates=[
                    "message",
                    "callback_query",
                    "chat_member"
                ]
            )
            
        except Exception as e:
            logger.error(f"Error while running bot: {e}")
            raise

async def main() -> int:
    """Main function"""
    bot_instance = MLBBBot()
    
    async with bot_instance.bot_context():
        try:
            await bot_instance.start()
            return 0
        except Exception as e:
            logger.critical(f"Critical error occurred: {e}")
            return 1

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
