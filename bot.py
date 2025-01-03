# bot.py
import asyncio
import logging
from aiogram import Bot, Dispatcher

from utils.db import async_session, init_db
from utils.models import User, Item
from handlers import base_router
from utils.settings import settings

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Ініціалізація бази даних
async def setup_database():
    try:
        await init_db()
        logger.info("База даних ініціалізована успішно")
    except Exception as e:
        logger.error(f"Помилка при ініціалізації бази даних: {e}")
        raise

# Ініціалізація бота та диспетчера
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# Реєстрація маршрутизаторів
dp.include_router(base_router)

async def main():
    try:
        # Ініціалізація бази даних
        await setup_database()
        
        # Старт бота
        logger.info("Бот запускається...")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Критична помилка: {e}")
        raise
    finally:
        await bot.close()
        logger.info("Бот зупинено")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот зупинено користувачем")
    except Exception as e:
        logger.error(f"Неочікувана помилка: {e}")
