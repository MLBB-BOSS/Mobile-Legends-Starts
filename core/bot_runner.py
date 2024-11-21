# core/bot_runner.py

import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.bot import DefaultBotProperties
import logging

# Імпортуємо ваші роутери
from handlers.menu_handlers import router as menu_router
from handlers.message_handlers import router as message_router
from handlers.start_command import router as start_router

# Зчитуємо токен бота з змінної середовища
API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not API_TOKEN:
    raise ValueError("Не встановлено змінну середовища TELEGRAM_BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    # Використовуємо DefaultBotProperties для встановлення parse_mode
    default_properties = DefaultBotProperties(parse_mode='HTML')
    bot = Bot(token=API_TOKEN, default=default_properties)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Реєструємо роутери
    dp.include_router(start_router)
    dp.include_router(menu_router)
    dp.include_router(message_router)

    try:
        logger.info("Бот стартував.")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())
