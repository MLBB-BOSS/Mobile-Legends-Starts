# core/bot_runner.py

import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.bot import DefaultBotProperties

from handlers import start_router  # Імпортуємо start_router

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Отримуємо токен бота
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not API_TOKEN:
    raise ValueError("Не знайдено TELEGRAM_BOT_TOKEN у змінних середовища!")

async def setup_bot_commands(bot: Bot):
    """
    Налаштовує доступні команди для бота.
    """
    commands = [
        BotCommand(command="/start", description="Запустити бота"),
        BotCommand(command="/help", description="Отримати довідку"),
    ]
    await bot.set_my_commands(commands)
    logger.info("Команди бота успішно встановлені.")

async def on_startup(dispatcher: Dispatcher, bot: Bot):
    """
    Викликається під час запуску бота.
    """
    await setup_bot_commands(bot)
    logger.info("Бот успішно запущено.")

async def main():
    """
    Основна функція для запуску бота.
    """
    bot = Bot(
        token=API_TOKEN,
        session=AiohttpSession(),
        default=DefaultBotProperties(parse_mode="HTML")
    )
    dp = Dispatcher()

    # Реєструємо обробник для /start
    dp.include_router(start_router)

    dp.startup.register(on_startup)

    logger.info("Запуск полінгу...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Бот зупинено!")
