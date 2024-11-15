import asyncio
import logging
from core.bot import bot, dp
from handlers.hero_commands import router as hero_router  # Оновлений імпорт

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
        dp.include_router(hero_router)  # Використовуємо hero_router замість bot_router
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
