import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
# from aiogram.contrib.middlewares.logging import LoggingMiddleware  # Видаляємо імпорт

from config import settings
from handlers import setup_handlers

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("bot")

# Окрема функція для створення бота і диспетчера
def create_bot_and_dispatcher() -> tuple[Bot, Dispatcher]:
    bot = Bot(
        token=settings.TELEGRAM_BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        session=AiohttpSession()  # Явна сесія для HTTP-запитів
    )
    dp = Dispatcher(storage=MemoryStorage())  # FSM сховище
    # dp.message.middleware(LoggingMiddleware())  # Видаляємо рядок з middleware
    return bot, dp

# Основна функція запуску бота
async def main():
    logger.info("Starting bot...")
    bot, dp = create_bot_and_dispatcher()

    # Підключення обробників
    setup_handlers(dp)

    # Використання асинхронного контекстного менеджера
    try:
        async with bot:
            logger.info("Bot is polling...")
            await dp.start_polling(bot)
    except (KeyboardInterrupt, SystemExit):
        logger.warning("Bot stopped manually.")
    except Exception as e:
        logger.error("Critical error occurred: %s", e, exc_info=True)
    finally:
        logger.info("Closing bot session...")
        if bot.session:
            await bot.session.close()

# Точка входу
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot has been stopped gracefully!")
