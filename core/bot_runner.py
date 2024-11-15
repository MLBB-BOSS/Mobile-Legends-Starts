import asyncio
import logging
from aiogram import Bot, Dispatcher
from core.bot import bot, dp
from handlers.hero_commands import router as hero_router
from handlers.start_command import router as start_router
from handlers.message_handlers import router as message_router

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

async def main():
    # Реєструємо роутери
    dp.include_router(start_router)
    dp.include_router(hero_router)
    dp.include_router(message_router)
    
    # Логуємо успішну реєстрацію роутерів
    logger.info("Роутери зареєстровано успішно")
    
    try:
        # Запускаємо бота
        logger.info("Запускаємо бота...")
        await dp.start_polling(bot, skip_updates=True)
    except Exception as e:
        logger.error(f"Помилка при запуску бота: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
