# bot.py

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage  # Додано для FSM
from config import settings
from handlers.base import setup_handlers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(
    token=settings.TELEGRAM_BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    session=AiohttpSession()  # Додано для явного визначення сесії
)
dp = Dispatcher(storage=MemoryStorage())  # Додано storage для FSM

async def main():
    logger.info("Starting bot...")
    try:
        setup_handlers(dp)
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Error while running bot: {e}")
    finally:
        if bot.session:
            await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped!")
