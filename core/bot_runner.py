# core/bot_runner.py
import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
import logging
import aiogram

# Встановлюємо рівень логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Перевірка версії aiogram
logger.info(f"aiogram version: {aiogram.__version__}")

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

# Отримуємо токен з змінних середовища
API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not API_TOKEN:
    logger.critical("Не встановлено змінну середовища TELEGRAM_BOT_TOKEN")
    raise ValueError("Не встановлено змінну середовища TELEGRAM_BOT_TOKEN")

async def setup_bot_commands(bot: Bot):
    """Встановлює команди бота"""
    commands = [
        ("start", "Запустити бота"),
        ("help", "Отримати допомогу"),
        ("menu", "Показати головне меню")
    ]
    await bot.set_my_commands(commands)

async def on_startup(bot: Bot):
    """Дії при запуску бота"""
    await setup_bot_commands(bot)
    logger.info("Бот успішно запущено")

async def on_shutdown(bot: Bot):
    """Дії при зупинці бота"""
    logger.warning("Бот зупиняється...")
    await bot.session.close()
    logger.info("Бот успішно зупинено")

async def main():
    # Створюємо об'єкт бота
    bot = Bot(
        token=API_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
            link_preview=False  # Вимикаємо превью посилань за замовчуванням
        )
    )
    
    try:
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

        # Реєструємо роутери
        for router in routers:
            dp.include_router(router)

        # Встановлюємо обробники подій старту та зупинки
        dp.startup.register(on_startup)
        dp.shutdown.register(on_shutdown)
        
        # Запускаємо поллінг
        await dp.start_polling(bot, allowed_updates=[
            "message",
            "callback_query",
            "chat_member",
            "my_chat_member"
        ])
        
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
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот зупинений користувачем")
    except Exception as e:
        logger.critical(f"Неочікувана помилка: {e}")
