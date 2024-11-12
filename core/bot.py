# core/bot.py
import os
import logging
from typing import Dict, Any
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor

from . import CoreConfig, get_app_state
from services import init_services

# Отримуємо токен бота
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not set in environment variables")

# Налаштування логування
logger = logging.getLogger(__name__)

# Ініціалізація бота і диспетчера
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Отримуємо стан додатку
app_state = get_app_state()

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    """Обробник команди /start"""
    try:
        user_service = app_state.get_service('user_service')
        if user_service:
            await user_service.create_user(
                telegram_id=message.from_user.id,
                username=message.from_user.username or "Anonymous"
            )
        
        await message.reply(
            "Вітаю! Я MLBB-BOSS бот для організації турнірів Mobile Legends. "
            "Використовуйте /help для перегляду доступних команд."
        )
        app_state.increment_processed_commands()
        
    except Exception as e:
        logger.error(f"Error in start command: {e}")
        await message.reply("Вибачте, сталася помилка. Спробуйте пізніше.")

@dp.message_handler(commands=['help'])
async def cmd_help(message: types.Message):
    """Обробник команди /help"""
    help_text = """
Доступні команди:
/start - Почати роботу з ботом
/help - Показати це повідомлення
/profile - Переглянути свій профіль
/heroes - Список героїв
/achievements - Ваші досягнення
/tournament - Інформація про поточний турнір
/rules - Правила участі
    """
    await message.reply(help_text)
    app_state.increment_processed_commands()

@dp.message_handler(commands=['stats'])
async def cmd_stats(message: types.Message):
    """Обробник команди /stats"""
    stats = app_state.get_stats()
    stats_text = (
        f"📊 Статистика бота:\n"
        f"⏱ Час роботи: {stats['uptime']}\n"
        f"👥 Активних користувачів: {stats['active_users']}\n"
        f"📝 Оброблено команд: {stats['processed_commands']}\n"
    )
    await message.reply(stats_text)
    app_state.increment_processed_commands()

async def on_startup(dp: Dispatcher):
    """Callback при запуску бота"""
    try:
        # Ініціалізуємо ядро
        await initialize_core()
        
        # Ініціалізуємо сервіси
        services = await init_services(None)  # Тут потрібно передати session
        
        # Реєструємо сервіси в стані додатку
        for name, service in services.items():
            app_state.register_service(name, service)
        
        logger.info("Bot started successfully")
        
    except Exception as e:
        logger.error(f"Error during bot startup: {e}")
        raise

async def on_shutdown(dp: Dispatcher):
    """Callback при зупинці бота"""
    try:
        # Закриваємо ядро
        await shutdown_core()
        
        # Закриваємо з'єднання з Telegram
        await bot.close()
        
        logger.info("Bot shutdown completed")
        
    except Exception as e:
        logger.error(f"Error during bot shutdown: {e}")
        raise

def run_bot():
    """Запуск бота"""
    try:
        executor.start_polling(
            dp,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True
        )
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise

if __name__ == '__main__':
    run_bot()
