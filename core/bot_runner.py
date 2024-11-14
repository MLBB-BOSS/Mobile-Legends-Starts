# core/bot_runner.py

import asyncio
import logging
import signal
from aiogram import Dispatcher, exceptions
from core.bot import dp, bot, on_startup, on_shutdown
from handlers.start_handler import register_handlers as register_start_handler  # Імпортуємо реєстрацію обробника для команди /start
import handlers.callback_handler
import handlers.help_handler
import handlers.heroes_info_handler
import handlers.info_handler
import handlers.leaderboard_handler
import handlers.profile_handler
import handlers.screenshot_handler
import handlers.hero_handler

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

def setup_handlers(dp: Dispatcher):
    """Функція для реєстрації всіх обробників"""
    # Реєструємо обробник для команди /start
    register_start_handler(dp)  
    
    # Перевіряємо наявність потрібних функцій у кожному обробнику перед реєстрацією
    if hasattr(handlers.callback_handler, 'some_callback_handler'):
        dp.register_message_handler(handlers.callback_handler.some_callback_handler)
    else:
        logger.warning("Обробник 'some_callback_handler' не знайдено в 'callback_handler'")

    if hasattr(handlers.help_handler, 'help_command'):
        dp.register_message_handler(handlers.help_handler.help_command)
    else:
        logger.warning("Обробник 'help_command' не знайдено в 'help_handler'")

    if hasattr(handlers.heroes_info_handler, 'heroes_info_command'):
        dp.register_message_handler(handlers.heroes_info_handler.heroes_info_command)
    else:
        logger.warning("Обробник 'heroes_info_command' не знайдено в 'heroes_info_handler'")

    if hasattr(handlers.info_handler, 'info_command'):
        dp.register_message_handler(handlers.info_handler.info_command)
    else:
        logger.warning("Обробник 'info_command' не знайдено в 'info_handler'")

    if hasattr(handlers.leaderboard_handler, 'leaderboard_command'):
        dp.register_message_handler(handlers.leaderboard_handler.leaderboard_command)
    else:
        logger.warning("Обробник 'leaderboard_command' не знайдено в 'leaderboard_handler'")

    if hasattr(handlers.profile_handler, 'profile_command'):
        dp.register_message_handler(handlers.profile_handler.profile_command)
    else:
        logger.warning("Обробник 'profile_command' не знайдено в 'profile_handler'")

    if hasattr(handlers.screenshot_handler, 'screenshot_command'):
        dp.register_message_handler(handlers.screenshot_handler.screenshot_command)
    else:
        logger.warning("Обробник 'screenshot_command' не знайдено в 'screenshot_handler'")

    if hasattr(handlers.hero_handler, 'hero_command'):
        dp.register_message_handler(handlers.hero_handler.hero_command)
    else:
        logger.warning("Обробник 'hero_command' не знайдено в 'hero_handler'")

async def start_bot():
    """Функція для запуску бота з обробкою перепідключення при мережевих помилках"""
    while True:
        try:
            await on_startup(dp)  # Викликається при запуску бота
            setup_handlers(dp)  # Реєстрація обробників
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
