import asyncio
import logging
import signal
from typing import Optional, Set
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

# Покращене налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('bot.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

class MLBBBot:
    """Головний клас бота MLBB"""
    
    def __init__(self):
        """Ініціалізація бота та його компонентів"""
        self.bot: Optional[Bot] = None
        self.dp: Optional[Dispatcher] = None
        self.message_manager: Optional[MessageManager] = None
        self._is_running: bool = False
        self._active_users: Set[int] = set()  # Для відстеження активних користувачів
        self._setup_bot()
        self._setup_dispatcher()
        self._setup_signal_handlers()

    def _setup_signal_handlers(self) -> None:
        """Налаштування обробників сигналів"""
        try:
            for sig in (signal.SIGINT, signal.SIGTERM):
                signal.signal(sig, self._handle_shutdown)
            logger.info("Signal handlers set up successfully")
        except Exception as e:
            logger.error(f"Failed to set up signal handlers: {e}")

    def _handle_shutdown(self, signum, frame) -> None:
        """Обробка сигналів завершення"""
        logger.info(f"Received signal {signum}. Starting graceful shutdown...")
        self._is_running = False

    def _setup_bot(self) -> None:
        """Налаштування екземпляра бота"""
        try:
            session = AiohttpSession()
            self.bot = Bot(
                token=settings.TELEGRAM_BOT_TOKEN,
                default=DefaultBotProperties(
                    parse_mode=ParseMode.HTML,
                    protect_content=True  # Захист контенту
                ),
                session=session
            )
            self.message_manager = MessageManager(self.bot)
            logger.info("Bot initialized successfully")
        except ValueError as e:
            logger.error(f"Invalid bot token: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to initialize bot: {e}")
            raise

    def _setup_dispatcher(self) -> None:
        """Налаштування диспетчера та реєстрація обробників"""
        try:
            self.dp = Dispatcher(storage=MemoryStorage())
            self._setup_middlewares()
            setup_handlers(self.dp, self.message_manager)
            logger.info("Dispatcher initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize dispatcher: {e}")
            raise

    def _setup_middlewares(self) -> None:
        """Налаштування проміжного ПЗ"""
        try:
            # Database middleware
            self.dp.message.middleware(DatabaseMiddleware(async_session))
            self.dp.callback_query.middleware(DatabaseMiddleware(async_session))
            
            # Можна додати інші middleware тут
            
            logger.info("Middlewares set up successfully")
        except Exception as e:
            logger.error(f"Failed to set up middlewares: {e}")
            raise

    @asynccontextmanager
    async def bot_context(self):
        """Контекстний менеджер для життєвого циклу бота"""
        try:
            self._is_running = True
            yield
        finally:
            self._is_running = False
            if self.bot and self.bot.session:
                await self.bot.session.close()
                logger.info("Bot session closed")

    async def create_tables(self) -> None:
        """Створення таблиць бази даних"""
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables created successfully")
        except SQLAlchemyError as e:
            logger.error(f"Failed to create database tables: {e}")
            raise

    async def _setup_database(self) -> None:
        """Налаштування бази даних"""
        try:
            await init_db()
            await self.create_tables()
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise

    def add_active_user(self, user_id: int) -> None:
        """Додати користувача до списку активних"""
        self._active_users.add(user_id)

    def remove_active_user(self, user_id: int) -> None:
        """Видалити користувача зі списку активних"""
        self._active_users.discard(user_id)

    @property
    def active_users_count(self) -> int:
        """Отримати кількість активних користувачів"""
        return len(self._active_users)

    async def start(self) -> None:
        """Запуск бота"""
        try:
            logger.info("Starting bot...")
            
            # Ініціалізація бази даних
            await self._setup_database()
            
            # Запуск поллінгу
            await self.dp.start_polling(
                self.bot,
                allowed_updates=[
                    "message",
                    "callback_query",
                    "chat_member",
                    "my_chat_member"  # Додано для відстеження змін статусу бота
                ]
            )
            
        except Exception as e:
            logger.error(f"Error while running bot: {e}")
            raise

async def main() -> int:
    """Головна функція"""
    bot_instance = MLBBBot()
    
    async with bot_instance.bot_context():
        try:
            await bot_instance.start()
            return 0
        except Exception as e:
            logger.critical(f"Critical error occurred: {e}", exc_info=True)
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
        logger.critical(f"Unexpected error occurred: {e}", exc_info=True)
        exit(1)
