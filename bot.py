import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from database import init_db, DatabaseMiddleware, async_session
from handlers.user_handlers import router as user_router
from config import settings

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ініціалізація бота та диспетчера
bot = Bot(token=settings.BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Реєстрація роутерів
dp.include_router(user_router)

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
