# bot.py
# Created: 2024-11-24
# Author: MLBB-BOSS
# Description: Головний файл бота з налаштуваннями та запуском

import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import settings
from handlers import register_handlers
from database import create_db_and_tables, DatabaseMiddleware

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)

logger = logging.getLogger(__name__)

async def main():
    try:
        # Перевіряємо наявність токену
        if not settings.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN не знайдено в змінних середовища")
            
        # Налаштування бота
        default_settings = DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
        
        # Ініціалізація бота
        bot = Bot(
            token=settings.TELEGRAM_BOT_TOKEN,
            default=default_settings
        )
        
        # Створення диспетчера
        dp = Dispatcher()

        # Підключення middleware
        dp.message.middleware(DatabaseMiddleware())
        dp.callback_query.middleware(DatabaseMiddleware())

        # Реєстрація хендлерів
        register_handlers(dp)

        # Ініціалізація бази даних
        await create_db_and_tables()

        logger.info("Бот успішно запущений")
        
        # Запуск бота
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"Помилка при запуску бота: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
