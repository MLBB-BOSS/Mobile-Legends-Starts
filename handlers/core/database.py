# core/database.py
from typing import Optional
import aiohttp
from motor.motor_asyncio import AsyncIOMotorClient
from logging import getLogger

logger = getLogger(__name__)

class Database:
    """Async database connection manager"""
    
    def __init__(self, mongo_url: str):
        self._url = mongo_url
        self._client: Optional[AsyncIOMotorClient] = None
        self._db = None
        self.logger = getLogger(__name__)

    async def connect(self) -> None:
        """Connect to database"""
        try:
            self._client = AsyncIOMotorClient(self._url)
            self._db = self._client.mlbb_bot
            
            # Verify connection
            await self._client.admin.command('ping')
            self.logger.info("Connected to MongoDB")
            
        except Exception as e:
            self.logger.error(f"Database connection error: {e}")
            raise

    async def close(self) -> None:
        """Close database connection"""
        if self._client:
            self._client.close()
            self.logger.info("Closed MongoDB connection")

    @property
    def db(self):
        """Get database instance"""
        if not self._db:
            raise RuntimeError("Database not connected")
        return self._db

# core/http_client.py
class HTTPClient:
    """Async HTTP client manager"""
    
    def __init__(self):
        self._session: Optional[aiohttp.ClientSession] = None
        self.logger = getLogger(__name__)

    async def connect(self) -> None:
        """Create HTTP session"""
        self._session = aiohttp.ClientSession()
        self.logger.info("Created HTTP session")

    async def close(self) -> None:
        """Close HTTP session"""
        if self._session:
            await self._session.close()
            self.logger.info("Closed HTTP session")

    @property
    def session(self) -> aiohttp.ClientSession:
        """Get session instance"""
        if not self._session:
            raise RuntimeError("HTTP session not created")
        return self._session

# core/bot.py
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from core.database import Database
from core.http_client import HTTPClient
from handlers import register_handlers
from middlewares import register_middlewares

class MLBBBot:
    """Main bot class"""
    
    def __init__(self, token: str, mongo_url: str):
        self.bot = Bot(token=token)
        self.storage = MemoryStorage()
        self.dp = Dispatcher(storage=self.storage)
        self.db = Database(mongo_url)
        self.http = HTTPClient()
        self.logger = getLogger(__name__)

    async def start(self) -> None:
        """Start bot"""
        try:
            # Connect to services
            await self.db.connect()
            await self.http.connect()
            
            # Register handlers and middlewares
            register_handlers(self.dp)
            register_middlewares(self.dp, self.db, self.http)
            
            # Start polling
            self.logger.info("Starting bot...")
            await self.dp.start_polling(self.bot)
            
        except Exception as e:
            self.logger.error(f"Error starting bot: {e}")
            raise
        finally:
            await self.stop()

    async def stop(self) -> None:
        """Stop bot"""
        try:
            # Close connections
            await self.db.close()
            await self.http.close()
            
            # Close bot session
            await self.bot.session.close()
            self.logger.info("Bot stopped")
            
        except Exception as e:
            self.logger.error(f"Error stopping bot: {e}")
            raise

# main.py
import asyncio
import logging
from core.bot import MLBBBot
from config import BOT_TOKEN, MONGO_URL

async def main():
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create and start bot
    bot = MLBBBot(BOT_TOKEN, MONGO_URL)
    await bot.start()

if __name__ == '__main__':
    asyncio.run(main())
