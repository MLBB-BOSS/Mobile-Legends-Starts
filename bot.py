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
from middlewares.database import DatabaseMiddleware

# Логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('bot.log', encoding='utf-8')
    ]
)
logger = logging.getLogger("MLBBBot")


class MLBBBot:
    """Головний клас бота MLBB"""

    def __init__(self):
        """Ініціалізація бота та його компонентів"""
        self.bot: Optional[Bot] = None
        self.dp: Optional[Dispatcher] = None
        self.message_manager: Optional[MessageManager] = None
        self._is_running: bool = False
        self._active_users: Set[int] = set()  # Відстеження активних користувачів
        self._initialize_components()

    def _initialize_components(self) -> None:
        """Ініціалізація компонентів бота"""
        self._setup_bot()
        self._setup_dispatcher()
        self._setup_signal_handlers()

    def _setup_signal_handlers(self) -> None:
        """Налаштування обробників сигналів"""
        for sig in (signal.SIGINT, signal.SIGTERM):
            signal.signal(sig, self._handle_shutdown)
        logger.info("Signal handlers set up successfully")

    def _handle_shutdown(self, signum, frame) -> None:
        """Обробка сигналів завершення"""
        logger.info(f"Received signal {signum}. Starting graceful shutdown...")
        self._is_running = False

    def _setup_bot(self) -> None:
        """Налаштування екземпляра бота"""
        session = AiohttpSession()
        self.bot = Bot(
            token=settings.TELEGRAM_BOT_TOKEN,
            default=DefaultBotProperties(
                parse_mode=ParseMode.HTML,
                protect_content=True
            ),
            session=session
        )
        self.message_manager = MessageManager(self.bot)
        logger.info("Bot initialized successfully")

    def _setup_dispatcher(self) -> None:
        """Налаштування диспетчера та реєстрація обробників"""
        self.dp = Dispatcher(storage=MemoryStorage())
        self._setup_middlewares()
        setup_handlers(self.dp, self.message_manager)
        logger.info("Dispatcher initialized successfully")

    def _setup_middlewares(self) -> None:
        """Налаштування проміжного ПЗ"""
        self.dp.message.middleware(DatabaseMiddleware(async_session))
        self.dp.callback_query.middleware(DatabaseMiddleware(async_session))
        logger.info("Middlewares set up successfully")

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

    async def _setup_database(self) -> None:
        """Налаштування бази даних"""
        await init_db()
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database initialized successfully")

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
        await self._setup_database()
        await self.dp.start_polling(
            self.bot,
            allowed_updates=["message", "callback_query", "chat_member", "my_chat_member"]
        )


async def main() -> int:
    """Головна функція"""
    bot_instance = MLBBBot()
    async with bot_instance.bot_context():
        await bot_instance.start()
    return 0


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.critical(f"Unexpected error occurred: {e}", exc_info=True)
        exit(1)
