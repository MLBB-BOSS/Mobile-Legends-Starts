# bot.py

import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from config import settings
from utils.db import engine, AsyncSessionLocal, Base
import handlers.profile  # Імпортуємо хендлери

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ініціалізація бота та диспетчера
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Додавання середовищ
dp.message.middleware(LoggingMiddleware())

# Регістрація маршрутизаторів
dp.include_router(handlers.profile.profile_router)

async def main():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())