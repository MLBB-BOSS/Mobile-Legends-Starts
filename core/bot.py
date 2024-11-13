# core/bot.py

import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config.settings import settings

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Ініціалізація бота та диспетчера з використанням MemoryStorage
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

async def on_startup(dp: Dispatcher):
    """Функція, що викликається при запуску бота"""
    logger.info("🚀 Бот запускається...")

async def on_shutdown(dp: Dispatcher):
    """Функція, що викликається при зупинці бота"""
    logger.info("🔄 Бот зупиняється...")
    await dp.storage.close()
    await dp.storage.wait_closed()
    await bot.close()
    logger.info("✅ Бот зупинено.")
