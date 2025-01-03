# bot.py
import asyncio
import logging
from aiogram import Bot, Dispatcher
from utils.settings import settings
from utils.db import init_db
from handlers.base import router

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Створення бота та диспетчера
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# Реєстрація роутерів
dp.include_router(router)

async def main():
    logger.info("Ініціалізація бази даних...")
    await init_db()
    logger.info("База даних ініціалізована успішно")
    
    logger.info("Запуск бота...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот зупинено")
