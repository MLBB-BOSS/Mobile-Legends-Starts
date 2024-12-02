# bot.py
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from config import TELEGRAM_BOT_TOKEN  # Імпорт із файлу config.py
from handlers import setup_handlers

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("BotLogger")

# Перевірка наявності токена
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не знайдено в середовищі або файлі .env")

# Ініціалізація бота
bot = Bot(
    token=TELEGRAM_BOT_TOKEN,
    session=AiohttpSession(),
    parse_mode=ParseMode.HTML,
)

# Ініціалізація диспетчера
dp = Dispatcher(storage=MemoryStorage())

async def main():
    """
    Основна функція для запуску бота.
    """
    logger.info("Запуск бота...")
    try:
        # Реєстрація хендлерів
        setup_handlers(dp)

        # Запуск polling
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Помилка під час роботи бота: {e}")
    finally:
        if bot.session:
            await bot.session.close()
        logger.info("Сесія бота закрита.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот зупинено!")
