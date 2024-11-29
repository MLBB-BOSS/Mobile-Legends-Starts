# bot.py

import asyncio
import logging
from aiogram import Bot, Application
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage  # Для FSM
from config import settings
from handlers.base import setup_handlers

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    # Імпортуємо aiogram для логування версії
    import aiogram
    logger.info(f"aiogram version: {aiogram.__version__}")

    # Ініціалізація бота
    bot = Bot(
        token=settings.TELEGRAM_BOT_TOKEN,
        parse_mode=ParseMode.HTML
        # Якщо потрібно, можна додати кастомну сесію
    )
    
    # Ініціалізація Application з ботом та зберіганням FSM
    app = Application.builder().bot(bot).storage(MemoryStorage()).build()
    
    # Налаштування обробників
    setup_handlers(app)
    
    # Запуск бота
    try:
        logger.info("Starting bot...")
        await app.start()
        # Запуск Polling
        await app.updater.start_polling()
        # Очікування завершення роботи
        await app.updater.idle()
    except Exception as e:
        logger.error(f"Error while running bot: {e}")
    finally:
        # Завершення роботи бота та закриття сесії
        await app.shutdown()
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped!")
