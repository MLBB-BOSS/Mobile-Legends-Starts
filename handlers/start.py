from aiogram import Router, F
from aiogram.types import Message
from keyboards.level1.main_menu import get_main_menu

router = Router()

@router.message(F.text == "/start")
async def start_handler(message: Message):
    """Обробник для команди /start"""
    await message.answer(
        "Привіт! Ласкаво просимо до бота. Оберіть опцію:",
        reply_markup=get_main_menu()  # Використовуємо звичайну клавіатуру
    )
