# main.py
import asyncio
import logging
from aiogram import Bot, Dispatcher
from core.config import settings
from services.database import init_db

# Налаштування логування
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

# Ініціалізація бота
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

async def main():
    # Ініціалізація бази даних
    if not await init_db():
        logger.error("Failed to initialize database")
        return
    
    # Запуск бота
    try:
        logger.info("Starting bot...")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())
