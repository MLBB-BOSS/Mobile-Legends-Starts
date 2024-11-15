import asyncio
import logging
import os
from core.bot import bot, dp
from handlers.hero_commands import router as hero_router
from handlers.start_command import router as start_router
from handlers.message_handlers import router as message_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def on_startup():
    # Реєструємо роутери
    dp.include_router(start_router)
    dp.include_router(hero_router)
    dp.include_router(message_router)
    logger.info("Бот запущений і готовий до роботи")

async def main():
    # Налаштування логування
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    # Запуск бота
    try:
        await dp.start_polling(bot, on_startup=on_startup)
    except Exception as e:
        logger.error(f"Помилка при запуску бота: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
