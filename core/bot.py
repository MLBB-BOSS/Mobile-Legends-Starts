# core/bot.py

import logging
from aiogram import Bot, Dispatcher
from config.settings import settings

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ініціалізація бота та диспетчера
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

async def on_startup(dp: Dispatcher):
    """Функція, що викликається при запуску бота"""
    logger.info("Бот запускається...")

async def on_shutdown(dp: Dispatcher):
    """Функція, що викликається при зупинці бота"""
    logger.info("Бот зупиняється...")
    await dp.storage.close()
    await dp.storage.wait_closed()
