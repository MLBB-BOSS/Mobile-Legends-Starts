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
from handlers.heroes import router as heroes_router
from handlers.guides import router as guides_router
from handlers.counter_picks import router as counter_picks_router
from handlers.builds import router as builds_router
from handlers.voting import router as voting_router
from handlers.profile import router as profile_router
from handlers.statistics import router as statistics_router
from handlers.achievements import router as achievements_router
from handlers.settings import router as settings_router
from handlers.feedback import router as feedback_router
from handlers.help import router as help_router

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ініціалізація бота
bot = Bot(
    token=settings.TELEGRAM_BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    session=AiohttpSession()  # Додано для явного визначення сесії
)

# Ініціалізація диспетчера з підтримкою FSM
dp = Dispatcher(storage=MemoryStorage())  # Додано storage для FSM

async def main():
    logger.info("Starting bot...")
    try:
        # Підключення базового маршрутизатора
        setup_handlers(dp)

        # Реєстрація інших маршрутизаторів
        dp.include_router(heroes_router)
        dp.include_router(guides_router)
        dp.include_router(counter_picks_router)
        dp.include_router(builds_router)
        dp.include_router(voting_router)
        dp.include_router(profile_router)
        dp.include_router(statistics_router)
        dp.include_router(achievements_router)
        dp.include_router(settings_router)
        dp.include_router(feedback_router)
        dp.include_router(help_router)

        # Запуск бота
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
