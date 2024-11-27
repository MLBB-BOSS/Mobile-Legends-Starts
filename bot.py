from aiogram import Bot, Dispatcher
from handlers import setup_handlers
from keyboards.level1.main_menu import get_main_menu
from aiogram.types import Message
from aiogram import Router, F
import os

# Токен
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не встановлено!")

# Створення бота
bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()

# Обробник команди /start
@router.message(F.text == "/start")
async def start_handler(message: Message):
    await message.answer(
        "Привіт! Ласкаво просимо до бота.",
        reply_markup=get_main_menu()
    )

# Реєструємо хендлери
dp.include_router(router)
setup_handlers(dp)

if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
