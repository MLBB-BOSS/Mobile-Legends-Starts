# core/bot_runner.py - головний файл запуску

import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
import logging

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Отримання токену бота з Heroku Config Vars
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not API_TOKEN:
    logger.critical("Не встановлено TELEGRAM_BOT_TOKEN")
    raise ValueError("Необхідно вказати TELEGRAM_BOT_TOKEN")

# Імпортуємо роутери
from handlers import start_handlers, menu_handlers, callback_handlers

async def setup_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Запустити бота"),
        BotCommand(command="help", description="Отримати допомогу"),
    ]
    await bot.set_my_commands(commands)

async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Реєструємо роутери
    dp.include_router(start_handlers.router)
    dp.include_router(menu_handlers.router)
    dp.include_router(callback_handlers.router)

    # Налаштування бота
    await setup_bot_commands(bot)

    logger.info("Бот запущено!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот зупинено.")
