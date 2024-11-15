import asyncio
import logging
from aiogram import Bot, Dispatcher
from core.bot import bot, dp
from handlers.hero_commands import router as hero_router
from handlers.start_command import router as start_router
from handlers.message_handlers import router as message_router
from services.database import init_db

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

async def main():
    try:
        # Ініціалізуємо базу даних
        logger.info("Ініціалізація бази даних...")
        await init_db()
        logger.info("База даних ініціалізована успішно")

        # Реєструємо роутери
        dp.include_router(start_router)
        dp.include_router(hero_router)
        dp.include_router(message_router)
        
        # Логуємо успішну реєстрацію роутерів
        logger.info("Роутери зареєстровано успішно")
        
        # Запускаємо бота
        logger.info("Запускаємо бота...")
        await dp.start_polling(bot, skip_updates=True)
        
    except Exception as e:
        logger.error(f"Критична помилка: {e}")
        raise
    finally:
        logger.info("Завершення роботи бота")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот зупинений вручну")
    except Exception as e:
        logger.error(f"Неочікувана помилка: {e}")
