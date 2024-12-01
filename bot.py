# bot.py

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from config import settings
from handlers.base import setup_handlers

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ініціалізація бота
try:
    bot = Bot(
        token=settings.TELEGRAM_BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        session=AiohttpSession()
    )
    logger.info("Bot instance created successfully.")
except Exception as e:
    logger.error(f"Error initializing bot: {e}")
    raise

# Ініціалізація диспетчера з підтримкою FSM
try:
    dp = Dispatcher(storage=MemoryStorage())
    logger.info("Dispatcher initialized with MemoryStorage.")
except Exception as e:
    logger.error(f"Error initializing dispatcher: {e}")
    raise

async def main():
    logger.info("Starting bot...")
    try:
        # Налаштування обробників
        logger.info("Setting up handlers...")
        setup_handlers(dp)

        # Запуск опитування
        logger.info("Starting polling...")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Critical error during bot operation: {e}")
    finally:
        logger.info("Shutting down bot session...")
        if bot.session:
            await bot.session.close()

if __name__ == "__main__":
    try:
        logger.info("Bot script started.")
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped manually.")
    except Exception as e:
        logger.error(f"Unhandled exception: {e}")
