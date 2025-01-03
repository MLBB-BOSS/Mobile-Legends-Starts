
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from utils.db import init_db, SessionLocal
from handlers.base import setup_handlers

from dotenv import load_dotenv
import os
import logging

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    # Ініціалізація бази даних
    await init_db()

    # Ініціалізація бота та диспетчера
    bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Налаштування обробників
    setup_handlers(dp)

    # Запуск бота
    try:
        await dp.start_polling(bot)
    finally:
        await bot.close()

if __name__ == "__main__":
    asyncio.run(main())
