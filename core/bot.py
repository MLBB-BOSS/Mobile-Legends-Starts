from aiogram import Bot, Dispatcher
from config.settings import settings

# Ініціалізація бота та диспетчера
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
