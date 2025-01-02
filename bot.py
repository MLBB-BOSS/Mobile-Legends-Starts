# bot.py

import logging
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from handlers import setup_handlers
import os

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ініціалізація бота
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Переконайтеся, що ви встановили BOT_TOKEN у змінних середовища
if not BOT_TOKEN:
    logger.error("BOT_TOKEN не встановлений у змінних середовища!")
    exit(1)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Реєстрація хендлерів
setup_handlers(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
