# bot.py

import logging
from aiogram import Bot, Dispatcher, executor
from aiogram.middleware.logging import LoggingMiddleware
from handlers import setup_handlers
from config import settings  # Імпорт налаштувань
import os

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Перевірка та валідація налаштувань
try:
    settings.validate()
except Exception as e:
    logger.error(f"Configuration error: {e}")
    exit(1)

# Ініціалізація бота
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)
dp.message.middleware.setup(LoggingMiddleware())

# Реєстрація хендлерів
setup_handlers(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
