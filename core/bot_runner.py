# core/bot_runner.py

import asyncio
import logging
import sys
from pathlib import Path
import os

# Якщо ви використовуєте python-dotenv для локальної розробки, розкоментуйте наступні рядки
# from dotenv import load_dotenv
# load_dotenv()

# Отримуємо токен бота з змінної середовища
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("Не вдалося знайти змінну середовища TELEGRAM_BOT_TOKEN")

# Додаємо шлях до кореневої директорії проекту
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.bot import bot, dp
from handlers.hero_commands import router as hero_router
from handlers.start_command import router as start_router
from handlers.message_handlers import router as message_router  # Додаємо імпорт message_router

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

async def on_startup():
    """Ініціалізація всіх необхідних налаштувань при запуску бота."""
    try:
        logger.info("🚀 Бот запускається...")
        # Підключаємо роутери
        dp.include_router(start_router)      # Стартовий роутер
        dp.include_router(hero_router)       # Роутер команд героїв
        dp.include_router(message_router)    # Роутер обробки повідомлень
        logger.info("✅ Роутери підключено успішно")
    except Exception as e:
        logger.error(f"❌ Помилка при ініціалізації: {e}")
        raise

async def on_shutdown():
    """Дії при завершенні роботи бота."""
    logger.info("🔄 Закриття з'єднань...")
    await bot.session.close()
    logger.info("✅ Бот успішно зупинено.")

async def main():
    """Головна функція запуску бота."""
    logger.info("📱 Початок роботи бота...")
    try:
        await dp.start_polling(
            bot,
            skip_updates=True,
            on_startup=on_startup,
            on_shutdown=on_shutdown
        )
    except Exception as e:
        logger.error(f"❌ Помилка під час роботи бота: {e}")
        raise
    finally:
        logger.info("🔄 Завершення роботи бота...")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Бот зупинено користувачем")
    except Exception as e:
        logger.error(f"❌ Критична помилка: {e}", exc_info=True)
        exit(1)
