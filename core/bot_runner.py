# core/bot_runner.py

import asyncio
import logging
from core.bot import bot, dp
from handlers.hero_handler import router as hero_router

logging.basicConfig(level=logging.INFO)

async def on_startup():
    """Ініціалізація всіх необхідних налаштувань при запуску бота."""
    logging.info("Бот запускається...")
    dp.include_router(hero_router)

async def main():
    await on_startup()
    try:
        async with dp.start_polling(bot):
            logging.info("Бот працює...")
    except Exception as e:
        logging.error(f"❌ Помилка під час роботи бота: {e}")
    finally:
        await bot.session.close()
        logging.info("Бот зупинено.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("👋 Бот зупинено користувачем.")
    except Exception as e:
        logging.error(f"❌ Несподівана помилка: {e}")
