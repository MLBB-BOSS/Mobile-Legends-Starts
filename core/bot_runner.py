# core/bot_runner.py

import asyncio
import logging
from core.bot import bot, dp
from handlers.hero_handler import router as hero_router

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

async def on_startup():
    """Ініціалізація всіх необхідних налаштувань при запуску бота."""
    logger.info("Бот запускається...")
    dp.include_router(hero_router)

async def main():
    await on_startup()
    try:
        logger.info("Початок роботи бота...")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"❌ Помилка під час роботи бота: {e}")
    finally:
        await bot.session.close()
        logger.info("Бот зупинено.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Бот зупинено користувачем.")
    except Exception as e:
        logger.error(f"❌ Несподівана помилка: {e}")
