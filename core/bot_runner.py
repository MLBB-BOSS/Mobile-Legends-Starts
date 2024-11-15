import asyncio
import logging
from core.bot import bot, dp
from handlers.hero_handler import router as hero_router

# Налаштування логування з відповідним форматом
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

async def on_startup():
    """Ініціалізація всіх необхідних налаштувань при запуску бота."""
    logger.info("Бот запускається...")
    dp.include_router(hero_router)  # Додаємо маршрутизатор обробників

async def main():
    logger.info("Початок роботи бота...")
    try:
        await dp.start_polling(
            bot,
            skip_updates=True,
            on_startup=on_startup
        )
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
