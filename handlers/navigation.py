from aiogram import Router, F
from aiogram.types import Message
from keyboards.level2.navigation_menu import get_navigation_menu

router = Router()

@router.message(F.text == "🧭 Навігація")
async def navigation_menu_handler(message: Message):
    """Обробник для меню Навігація"""
    await message.answer(
        "🧭 Навігація: Оберіть потрібний розділ:",
        reply_markup=get_navigation_menu()
    )
