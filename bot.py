# bot.py

import logging
import asyncio
from aiogram import Bot, Dispatcher
from handlers import setup_handlers
from config import settings

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
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

    # Реєстрація хендлерів
    setup_handlers(dp)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
