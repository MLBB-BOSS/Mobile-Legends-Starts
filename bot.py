# bot.py

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage  # Для FSM
from config import settings
from handlers.ai_handler import router as ai_router  # AI-роутер
from handlers.base import setup_handlers  # Функція для підключення базового роутера

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ініціалізація бота
bot = Bot(
    token=settings.TELEGRAM_BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    session=AiohttpSession()
)

# Ініціалізація диспетчера з підтримкою FSM
dp = Dispatcher(storage=MemoryStorage())

async def main():
    logger.info("Starting bot...")
    try:
        dp.include_router(ai_router)  # Підключаємо AI-роутер першочергово
        setup_handlers(dp)  # Підключаємо базовий роутер
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
