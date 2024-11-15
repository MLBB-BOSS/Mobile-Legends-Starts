import asyncio
import logging
import os
import sys
from pathlib import Path

# Додаємо шлях до кореневої директорії проекту
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent
sys.path.insert(0, str(project_root))

try:
    from core.bot import bot, dp
    from handlers.hero_commands import router as hero_router
except ModuleNotFoundError as e:
    print(f"Error importing modules: {e}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    raise

# Налаштування логування з відповідним форматом
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

async def on_startup():
    """Ініціалізація всіх необхідних налаштувань при запуску бота."""
    try:
        logger.info("🚀 Бот запускається...")
        # Виводимо інформацію про шляхи для діагностики
        logger.info(f"Working directory: {os.getcwd()}")
        logger.info(f"Project root: {project_root}")
        dp.include_router(hero_router)
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
