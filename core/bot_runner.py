# core/bot_runner.py

import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.bot import DefaultBotProperties
import logging

API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')  # Використовуйте правильну назву

if not API_TOKEN:
    raise ValueError("Не встановлено змінну середовища TELEGRAM_BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    default_properties = DefaultBotProperties(parse_mode='HTML')
    bot = Bot(token=API_TOKEN, default=default_properties)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Реєструємо роутери
    # dp.include_router(...)

    try:
        logger.info("Бот стартував.")
        await dp.start_polling(bot)
    finally:
        await bot.close()

if __name__ == '__main__':
    asyncio.run(main())
