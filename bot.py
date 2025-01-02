# bot.py

import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.middleware.logging import LoggingMiddleware
from handlers import setup_handlers
from config import settings

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    # Перевірка та валідація налаштувань
    try:
        settings.validate()
    except Exception as e:
        logger.error(f"Configuration error: {e}")
        return

    # Ініціалізація бота
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    dp = Dispatcher()

    # Додавання middlewares
    dp.message.middleware.setup(LoggingMiddleware())

    # Реєстрація хендлерів
    setup_handlers(dp)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
