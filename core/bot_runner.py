# core/bot_runner.py

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers.menu_handlers import router as menu_router
from handlers.message_handlers import router as message_router  # Припустимо, ви маєте інший роутер
import logging

API_TOKEN = 'TELEGRAM_BOT_TOKEN'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    bot = Bot(token=API_TOKEN, parse_mode='HTML')
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Реєструємо роутери
    dp.include_router(menu_router)
    dp.include_router(message_router)

    try:
        logger.info("Бот стартував.")
        await dp.start_polling(bot)
    finally:
        await bot.close()

if __name__ == '__main__':
    asyncio.run(main())
