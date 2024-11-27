import logging
from aiogram import Bot, Dispatcher
from handlers import setup_handlers
from keyboards.level1.main_menu import get_main_menu
from aiogram.types import Message
from aiogram import Router, F
import os

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    logger.error("Змінна оточення TELEGRAM_BOT_TOKEN не задана!")
    raise ValueError("TELEGRAM_BOT_TOKEN не встановлено!")

logger.info("Запуск бота...")

# Створення бота
bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()

# Обробник команди /start
@router.message(F.text == "/start")
async def start_handler(message: Message):
    logger.info(f"Користувач {message.from_user.id} надіслав команду /start")
    await message.answer(
        "Привіт! Ласкаво просимо до бота.",
        reply_markup=get_main_menu()
    )

# Реєструємо хендлери
dp.include_router(router)
setup_handlers(dp)

if __name__ == "__main__":
    import asyncio
    try:
        asyncio.run(dp.start_polling(bot))
    except Exception as e:
        logger.exception(f"Виникла помилка: {e}")
