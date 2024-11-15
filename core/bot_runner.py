import asyncio
import logging
from core.bot import bot, dp
from heroes.hero_handlers import router as hero_router

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

async def on_startup():
    """Ініціалізація при запуску бота."""
    logger.info("🚀 Бот запускається...")
    # Реєструємо роутер перед стартом
    dp.include_router(hero_router)
    logger.info("✅ Роутери зареєстровано")

async def main():
    logger.info("Початок роботи бота...")
    try:
        # Важливо: on_startup має викликатись до start_polling
        await on_startup()
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"❌ Помилка під час роботи бота: {e}")
    finally:
        logger.info("Бот зупинено.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Бот зупинено користувачем.")
    except Exception as e:
        logger.error(f"❌ Несподівана помилка: {e}")
