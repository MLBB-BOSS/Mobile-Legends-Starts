# core/bot_runner.py

import asyncio
import logging
import signal
from aiogram import Dispatcher, exceptions
from core.bot import dp, bot, on_startup, on_shutdown
import handlers.callback_handler
import handlers.help_handler
import handlers.heroes_info_handler
import handlers.info_handler
import handlers.leaderboard_handler
import handlers.profile_handler
import handlers.screenshot_handler

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

async def start_bot():
    """Функція для запуску бота з обробкою перепідключення при мережевих помилках"""
    while True:
        try:
            await on_startup(dp)  # Викликається при запуску бота
            await dp.start_polling(timeout=10)  # Налаштовано таймаут у 10 секунд
        except exceptions.NetworkError as e:
            logger.error(f"Network error occurred: {e}")
            await asyncio.sleep(5)  # Чекаємо 5 секунд перед повторним підключенням
        except Exception as e:
            logger.error(f"❌ Помилка при роботі бота: {e}", exc_info=True)
        finally:
            await shutdown()
            break  # Вихід з циклу після коректного завершення роботи

async def main():
    """Головна функція для обробки сигналів та запуску бота"""
    # Реєстрація обробників сигналів
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, signal_handler)

    await start_bot()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Бот зупинено користувачем.")
    except Exception as e:
        logger.error(f"❌ Несподівана помилка: {e}", exc_info=True)
