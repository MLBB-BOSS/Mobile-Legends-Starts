import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from database import init_db, DatabaseMiddleware, async_session
from handlers import setup_handlers
from config import settings

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ініціалізація бота та диспетчера
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Реєстрація хендлерів
setup_handlers(dp)

# Реєстрація middleware
dp.update.middleware(DatabaseMiddleware(async_session))

async def main():
    logger.info("Запуск бота...")
    
    # Ініціалізація бази даних
    await init_db()
    
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот зупинено.")
