import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import config
from handlers.start_command import router as start_router
from handlers.hero_commands import router as hero_router
from handlers.message_handlers import router as message_router
from handlers.menu_handlers import router as menu_router
from handlers.statistics_handler import router as statistics_router  # Add this
from handlers.hero_class_handlers import router as hero_class_router  # Add this

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Ініціалізація бота і диспетчера
bot = Bot(token=config.TELEGRAM_BOT_TOKEN.get_secret_value())
dp = Dispatcher()

def setup_routers() -> None:
    logger.info("Починаємо реєстрацію роутерів...")
    
    # Order matters - more specific handlers should go first
    dp.include_router(statistics_router)     # Add statistics router
    dp.include_router(hero_class_router)     # Add hero class router
    dp.include_router(menu_router)
    dp.include_router(start_router)
    dp.include_router(hero_router)
    dp.include_router(message_router)         # Keep this last as fallback
    
    logger.info("Всі роутери зареєстровано")

async def main() -> None:
    try:
        setup_routers()
        logger.info("Запускаємо бота...")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Помилка при запуску бота: {e}")
        raise
    finally:
        logger.info("Закриваємо з'єднання з Telegram...")
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот зупинений користувачем")
    except Exception as e:
        logger.error(f"Критична помилка: {e}")
        raise
