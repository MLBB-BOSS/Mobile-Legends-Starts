# /bot.py
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from handlers import setup_handlers

TOKEN = "ВАШ_ТОКЕН_БОТА"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Налаштовуємо всі хендлери
setup_handlers(dp)

@dp.message(F.text == "/start")
async def start_handler(message: Message):
    from keyboards.level1.main_menu import get_main_menu
    await message.answer(
        "Привіт! Ласкаво просимо до бота.",
        reply_markup=get_main_menu()
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
