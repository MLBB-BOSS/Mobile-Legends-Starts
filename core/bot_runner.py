import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import BotCommand, BotCommandScopeDefault
import logging
from dotenv import load_dotenv  # Для роботи з .env

# Завантажуємо змінні середовища
load_dotenv()

# Встановлюємо рівень логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Перевірка версії aiogram
import aiogram
logger.info(f"aiogram version: {aiogram.__version__}")

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
    try:
        commands = [
            BotCommand(command="start", description="Запустити бота"),
            BotCommand(command="help", description="Отримати допомогу"),
            BotCommand(command="menu", description="Показати головне меню")
        ]
        
        await bot.set_my_commands(
            commands=commands,
            scope=BotCommandScopeDefault()
        )
        logger.info("Команди бота успішно встановлені")
    except Exception as e:
        logger.error(f"Помилка при встановленні команд бота: {e}")
        raise

async def on_startup(bot: Bot):
    """Дії при запуску бота"""
    try:
        await setup_bot_commands(bot)
        logger.info("Бот успішно запущено")
    except Exception as e:
        logger.error(f"Помилка при запуску бота: {e}")
        raise

async def on_shutdown(bot: Bot):
    """Дії при зупинці бота"""
    try:
        logger.warning("Бот зупиняється...")
        await bot.session.close()
        logger.info("Бот успішно зупинено")
    except Exception as e:
        logger.error(f"Помилка при зупинці бота: {e}")

async def main():
    try:
        # Створюємо об'єкт бота
        bot = Bot(
            token=API_TOKEN,
            default=DefaultBotProperties(
                parse_mode=ParseMode.HTML,
                link_preview=False
            )
        )
        
        # Ініціалізуємо сховище та диспетчер
        storage = MemoryStorage()
        dp = Dispatcher(storage=storage)

        # Реєструємо всі роутери
        routers = [
            start_router,
            menu_router,
            message_router,
            error_router,
            hero_class_router,
            hero_router,
            navigation_router
        ]

        for router in routers:
            dp.include_router(router)

        # Встановлюємо обробники подій старту та зупинки
        dp.startup.register(on_startup)
        dp.shutdown.register(on_shutdown)
        
        # Запускаємо поллінг
        logger.info("Запуск бота...")
        await dp.start_polling(
            bot,
            allowed_updates=[
                "message",
                "callback_query",
                "chat_member",
                "my_chat_member"
            ]
        )
        
    except Exception as e:
        logger.exception(f"Критична помилка: {e}")
        raise
        
    finally:
        if 'bot' in locals():
            await bot.session.close()
            logger.info("З'єднання з Telegram API закрито")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот зупинений користувачем")
    except Exception as e:
        logger.critical(f"Неочікувана помилка: {e}")
        raise
