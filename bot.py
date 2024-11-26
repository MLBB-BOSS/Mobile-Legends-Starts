from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message
from keyboards.level1.main_menu import get_main_menu
import os

# Отримуємо токен з змінної оточення
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не встановлено в змінних оточення!")

# Створюємо екземпляр бота
bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()

# Головний обробник для команди /start
@router.message(F.text == "/start")
async def start_handler(message: Message):
    """Обробник для команди /start"""
    await message.answer(
        "Привіт! Ласкаво просимо до бота.",
        reply_markup=get_main_menu()
    )

# Реєструємо маршрутизатор у Dispatcher
dp.include_router(router)

if __name__ == "__main__":
    import asyncio

    # Запускаємо бот у режимі polling
    try:
        asyncio.run(dp.start_polling(bot))
    except (KeyboardInterrupt, SystemExit):
        print("Бот зупинено!")
