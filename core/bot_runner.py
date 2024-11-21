import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from handlers.start_command import router as start_router
from handlers.navigation_handlers import router as navigation_router

API_TOKEN = "ВАШ_TELEGRAM_BOT_TOKEN"  # Замініть на ваш токен

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def setup_bot_commands(bot: Bot):
    """Налаштування команд бота"""
    commands = [
        BotCommand(command="/start", description="Запустити бота"),
    ]
    await bot.set_my_commands(commands)

async def on_startup(dispatcher: Dispatcher, bot: Bot):
    """Дії при запуску бота"""
    await setup_bot_commands(bot)
    logger.info("Бот запущено.")

async def main():
    """Основна функція для запуску бота"""
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()

    # Реєструємо роутери
    dp.include_router(start_router)
    dp.include_router(navigation_router)

    dp.startup.register(on_startup)

    logger.info("Запуск полінгу...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот зупинено.")
