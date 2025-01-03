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

# Ініціалізація бази даних
async def setup_database():
    await init_db()

# Ініціалізація бота та диспетчера
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

# Реєстрація маршрутизаторів
dp.include_router(base_router)

async def main():
    # Ініціалізація бази даних
    await setup_database()
    logger.info("База даних ініціалізована.")
    
    # Старт бота
    try:
        await dp.start_polling()
    finally:
        await bot.close()

if __name__ == '__main__':
    asyncio.run(main())
