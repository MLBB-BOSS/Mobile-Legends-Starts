from aiogram import Router, F
from aiogram.types import Message
from keyboards.level3.guides_menu import get_guides_menu

router = Router()

@router.message(F.text == "📚 Гайди")
async def guides_menu_handler(message: Message):
    """Обробник для меню гайдів"""
    await message.answer(
        "📚 Гайди: Оберіть потрібний розділ.",
        reply_markup=get_guides_menu()
    )
