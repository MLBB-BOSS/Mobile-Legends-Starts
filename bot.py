# bot.py
import asyncio
from aiogram import Bot, Dispatcher, types
import logging
import os

from utils.db import async_session, init_db
from utils.models import User, Item
from handlers import base_router
from utils.settings import settings

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Функція для ініціалізації бази даних
async def setup_database():
    await init_db()
    logger.info("База даних ініціалізована успішно.")

# Ініціалізація бота з токеном з налаштувань
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

# Реєстрація маршрутизаторів
dp.include_router(base_router)

async def main():
    # Ініціалізація бази даних
    await setup_database()

    # Запуск бота
    try:
        logger.info("Бот запускається...")
        await dp.start_polling()
    finally:
        await bot.close()
        logger.info("Бот зупинено.")

if __name__ == '__main__':
    asyncio.run(main())
