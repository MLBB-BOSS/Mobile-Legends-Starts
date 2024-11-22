import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.client.session.default import DefaultBotProperties  # Новий імпорт для властивостей

from handlers.start_command import router as start_router
from handlers.navigation_handlers import router as navigation_router
from handlers.profile_handlers import router as profile_router  # Додано для профілю

# Отримуємо токен з середовища
API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Перевірка токена
if not API_TOKEN:
    raise ValueError("Не знайдено TELEGRAM_BOT_TOKEN у перемінних середовища!")

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def setup_bot_commands(bot: Bot):
    """Налаштування команд бота"""
    commands = [
        BotCommand(command="/start", description="Запустити бота"),
        BotCommand(command="/help", description="Отримати довідку"),
    ]
    await bot.set_my_commands(commands)
    logger.info("Команди бота успішно встановлені.")


async def on_startup(dispatcher: Dispatcher, bot: Bot):
    """Дії при запуску бота"""
    await setup_bot_commands(bot)
    logger.info("Бот успішно запущено.")


async def main():
    """Основна функція для запуску бота"""
    bot = Bot(
        token=API_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML")  # Новий спосіб налаштування parse_mode
    )
    dp = Dispatcher()

    # Реєструємо роутери
    dp.include_router(start_router)
    dp.include_router(navigation_router)
    dp.include_router(profile_router)  # Додано для профілю

    dp.startup.register(on_startup)

    logger.info("Запуск полінгу...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот зупинено.")
