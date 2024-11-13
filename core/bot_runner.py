# core/bot_runner.py

import asyncio
import logging
import signal
from aiogram import Dispatcher
from core.bot import dp, bot, on_startup, on_shutdown
import handlers.basic_handlers
import handlers.help_handler
import handlers.screenshot_handler
import handlers.heroes_info_handler
import handlers.leaderboard_handler
import handlers.profile_handler
import core.callback_handler

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def shutdown():
    """Функція для коректного завершення роботи бота"""
    logger.info("🔄 Початок послідовності завершення роботи...")
    await on_shutdown(dp)
    logger.info("✅ Завершення роботи бота успішно виконано.")

def signal_handler():
    """Обробник сигналів завершення роботи"""
    asyncio.create_task(shutdown())

async def main():
    """Головна функція запуску бота"""
    await on_startup(dp)

    # Реєстрація обробників сигналів
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, signal_handler)

    try:
        # Запуск бота на прослуховування
        await dp.start_polling()
    except Exception as e:
        logger.error(f"❌ Помилка при роботі бота: {e}", exc_info=True)
    finally:
        await shutdown()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Бот зупинено користувачем.")
    except Exception as e:
        logger.error(f"❌ Несподівана помилка: {e}", exc_info=True)
