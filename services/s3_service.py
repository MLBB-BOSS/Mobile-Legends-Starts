import os
import asyncio
import logging
from core.bot import run_bot
from core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Отримуємо DATABASE_URL з Heroku або локального .env
database_url = os.getenv('DATABASE_URL')
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql+asyncpg://', 1)

# Створюємо engine для бази даних
engine = create_async_engine(
    database_url or settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10
)

# Створюємо фабрику сесій
AsyncSessionFactory = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db():
    """Ініціалізація бази даних"""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(lambda x: x)
        logger.info("Database connection established successfully")
    except Exception as e:
        logger.error(f"Error connecting to database: {e}")
        raise

async def main():
    """Головна функція запуску"""
    try:
        # Ініціалізуємо базу даних
        await init_db()
        
        # Запускаємо бота
        await run_bot(AsyncSessionFactory)
        
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise
    finally:
        # Закриваємо з'єднання з базою даних
        await engine.dispose()

if __name__ == "__main__":
    try:
        # Встановлюємо правильний часовий пояс
        os.environ['TZ'] = 'UTC'
        
        # Запускаємо головну функцію
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
