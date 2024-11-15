import asyncio
import logging
import os
from core.bot import bot, dp
from handlers.hero_commands import router as hero_router
from handlers.start_command import router as start_router
from handlers.message_handlers import router as message_router

# Отримуємо токен бота із змінної середовища
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("Не вдалося знайти TELEGRAM_BOT_TOKEN у змінних середовища!")

# Налаштування логування
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

async def on_startup():
    dp.include_router(start_router)
    dp.include_router(hero_router)
    dp.include_router(message_router)
    logger.info("✅ Бот готовий до роботи.")

async def main():
    try:
        await dp.start_polling(bot, skip_updates=True, on_startup=on_startup)
    except Exception as e:
        logger.error(f"❌ Критична помилка: {e}", exc_info=True)

if __name__ == "__main__":
    asyncio.run(main())
