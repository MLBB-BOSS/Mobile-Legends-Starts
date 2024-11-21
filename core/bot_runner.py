import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import BotCommand, BotCommandScopeDefault
import logging
from dotenv import load_dotenv

# Завантажуємо змінні середовища
load_dotenv()

# Встановлюємо рівень логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Отримуємо токен з змінних середовища
API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not API_TOKEN:
    logger.critical("Не встановлено змінну середовища TELEGRAM_BOT_TOKEN")
    raise ValueError("Не встановлено змінну середовища TELEGRAM_BOT_TOKEN")

# Імпортуємо роутери
from handlers import (
    start_router,
    menu_router,
    message_router,
    error_router,
    hero_class_router,
    hero_router,
    navigation_router
)

async def setup_bot_commands(bot: Bot):
    """Встановлює команди бота"""
    commands = [
        BotCommand(command="start", description="Запустити бота"),
        BotCommand(command="help", description="Отримати допомогу"),
        BotCommand(command="menu", description="Показати головне меню")
    ]
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())
    logger.info("Команди бота успішно встановлені")

async def on_startup(bot: Bot):
    """Дії при запуску бота"""
    await setup_bot_commands(bot)
    logger.info("Бот успішно запущено")

async def on_shutdown(bot: Bot):
    """Дії при зупинці бота"""
    await bot.session.close()
    logger.info("Бот успішно зупинено")

async def main():
    bot = Bot(
        token=API_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
            link_preview=False
        )
    )
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Реєструємо всі роутери
    dp.include_router(start_router)
    dp.include_router(menu_router)
    dp.include_router(message_router)
    dp.include_router(error_router)
    dp.include_router(hero_class_router)
    dp.include_router(hero_router)
    dp.include_router(navigation_router)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    logger.info("Запуск бота...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот зупинений користувачем")
    except Exception as e:
        logger.critical(f"Критична помилка: {e}")
