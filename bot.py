# bot.py
# Created: 2024-11-24
# Author: MLBB-BOSS
# Description: Головний файл бота для управління турнірами Mobile Legends

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import settings
from handlers import register_all_handlers
from database import create_tables

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    try:
        # Ініціалізація бота та диспетчера
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN, parse_mode=ParseMode.HTML)
        dp = Dispatcher(storage=MemoryStorage())
        
        # Реєстрація всіх хендлерів
        register_all_handlers(dp)
        
        # Створення таблиць бази даних
        await create_tables()
        
        logger.info("Bot started successfully!")
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
    finally:
        if 'bot' in locals():
            await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
