# core/bot.py

import logging
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties  # Оптимізований імпорт
from aiogram.fsm.storage.memory import MemoryStorage
from config.settings import settings

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Ініціалізація бота з використанням DefaultBotProperties для встановлення parse_mode
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
