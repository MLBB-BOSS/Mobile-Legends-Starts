# /bot.py
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from handlers.main_menu import router as main_menu_router
from handlers.navigation import router as navigation_router
from handlers.heroes import router as heroes_router
import os

# Отримуємо токен з змінної оточення
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не встановлено в змінних оточення!")

# Створюємо екземпляр бота та диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Підключення обробників (routers)
dp.include_router(main_menu_router)
dp.include_router(navigation_router)
dp.include_router(heroes_router)

# Головний обробник для команди /start
@dp.message(commands=["start"])
async def start_handler(message: Message):
    from keyboards.level1.main_menu import get_main_menu
    await message.answer(
        "Привіт! Ласкаво просимо до бота.",
        reply_markup=get_main_menu()
    )

if __name__ == "__main__":
    import asyncio

    # Запускаємо бот у режимі polling
    asyncio.run(dp.start_polling(bot))
