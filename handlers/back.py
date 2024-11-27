from aiogram import Router, F
from aiogram.types import Message
from keyboards.level1.main_menu import get_main_menu

router = Router()

@router.message(F.text == "🔄 Назад")
async def back_to_main_menu(message: Message):
    """Обробник для повернення до головного меню"""
    await message.answer(
        "Ви повернулися до головного меню.",
        reply_markup=get_main_menu()
    )
