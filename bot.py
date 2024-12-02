import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from bot_config import settings  # Змінив імпорт на bot_config
from handlers.base import setup_handlers

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("BotLogger")

# Ініціалізація бота
bot = Bot(
    token=settings.TELEGRAM_BOT_TOKEN,
    session=AiohttpSession(),  # Явне визначення сесії
    parse_mode=ParseMode.HTML,  # Встановлено режим парсингу HTML
)

# Ініціалізація диспетчера з підтримкою FSM
dp = Dispatcher(storage=MemoryStorage())  # Використовуємо MemoryStorage для FSM

async def main():
    """
    Основна функція для запуску бота.
    """
    logger.info("Запуск бота...")
    try:
        # Налаштування обробників
        setup_handlers(dp)

        # Запуск polling
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Помилка під час роботи бота: {e}")
    finally:
        # Закриваємо сесію бота
        if bot.session:
            await bot.session.close()
        logger.info("Сесія бота закрита.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот зупинено!")
