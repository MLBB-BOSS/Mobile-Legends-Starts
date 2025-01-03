# bot.py
import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
import logging

# Імпортуємо роутери
from handlers.base import router as base_router
from handlers.main_menu import router as main_menu_router
from handlers.profile import router as profile_router
# Імпортуйте інші роутери за потребою

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Завантажте змінні середовища з .env файлу
load_dotenv()

# Отримайте токен бота з змінної середовища
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not TELEGRAM_BOT_TOKEN:
    logger.critical("Не встановлено змінну середовища TELEGRAM_BOT_TOKEN")
    exit(1)

# Створіть екземпляри бота та диспетчера
bot = Bot(token=TELEGRAM_BOT_TOKEN, parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Включіть всі роутери до диспетчера
dp.include_router(base_router)
dp.include_router(main_menu_router)
dp.include_router(profile_router)
# Включіть інші роутери за потребою

async def main():
    try:
        # Запустіть диспетчер
        await dp.start_polling(bot)
    finally:
        await bot.close()

if __name__ == '__main__':
    asyncio.run(main())