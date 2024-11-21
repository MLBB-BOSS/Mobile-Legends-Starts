# File: core/bot_runner.py

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router
from handlers.start_command import router as start_router
from handlers.hero_commands import router as hero_router
from handlers.message_handlers import router as message_router
from handlers.menu_handlers import router as menu_router
from handlers.error_handler import router as error_router
from dotenv import load_dotenv
import os

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Завантаження перемінних середовища з .env файлу
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    logger.error("BOT_TOKEN не встановлено у перемінних середовища!")
    exit(1)

# Ініціалізація бота та диспетчера
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Створення основного роутера
main_router = Router()

# Включення всіх роутерів
main_router.include_router(start_router)
main_router.include_router(hero_router)
main_router.include_router(menu_router)
main_router.include_router(message_router)
main_router.include_router(error_router)

def setup_routers() -> None:
    logger.info("Починаємо реєстрацію роутерів...")
    dp.include_router(main_router)
    logger.info("Всі роутери зареєстровано")

# Функція запуску бота
async def main() -> None:
    setup_routers()
    logger.info("Запускаємо бота...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот зупинений користувачем")
    except Exception as e:
        logger.error(f"Виникла непередбачена помилка: {e}")
