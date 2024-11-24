# bot.py
# Created: 2024-11-24
# Author: MLBB-BOSS
# Description: Головний файл бота з налаштуваннями та запуском

import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.fsm.storage.memory import MemoryStorage

from config import settings
from handlers.main_menu import router as main_menu_router
from handlers.navigation import router as navigation_router
from handlers.user_handlers import router as user_router
from database import create_db_and_tables, DatabaseMiddleware

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)

logger = logging.getLogger(__name__)

async def register_all_routers(dp: Dispatcher) -> None:
    """Реєстрація всіх роутерів"""
    routers = [
        main_menu_router,
        navigation_router,
        user_router,
    ]
    for router in routers:
        dp.include_router(router)
    logger.info("Всі роутери успішно зареєстровано")

async def setup_bot_commands(bot: Bot) -> None:
    """Налаштування команд бота"""
    commands = [
        ("start", "Запустити бота"),
        ("help", "Отримати допомогу"),
        ("menu", "Головне меню"),
        ("profile", "Мій профіль"),
        ("navigation", "Навігація по контенту")
    ]
    await bot.set_my_commands(commands)
    logger.info("Команди бота налаштовано")

async def main():
    try:
        # Перевіряємо наявність токену
        if not settings.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN не знайдено в змінних середовища")
            
        # Налаштування бота
        session = AiohttpSession()
        bot = Bot(
            token=settings.TELEGRAM_BOT_TOKEN,
            parse_mode=ParseMode.HTML,
            session=session
        )
        
        # Ініціалізація диспетчера зі сховищем станів
        dp = Dispatcher(storage=MemoryStorage())

        # Підключення middleware
        dp.update.middleware(DatabaseMiddleware())

        # Реєстрація роутерів
        await register_all_routers(dp)
        
        # Налаштування команд бота
        await setup_bot_commands(bot)

        # Ініціалізація бази даних
        await create_db_and_tables()

        logger.info("Бот успішно запущений")
        
        # Запуск бота
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"Помилка при запуску бота: {e}")
        sys.exit(1)
    finally:
        # Закриття сесії при завершенні
        if 'bot' in locals():
            await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот зупинений")
