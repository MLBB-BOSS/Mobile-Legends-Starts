# core/bot_runner.py

import asyncio
import logging
from aiogram import Dispatcher
from core.bot import bot, dp
from handlers.handlers import router

logging.basicConfig(level=logging.INFO)

async def on_startup():
    dp.include_router(router)

async def main():
    await on_startup()
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"❌ Помилка під час запуску бота: {e}")
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
