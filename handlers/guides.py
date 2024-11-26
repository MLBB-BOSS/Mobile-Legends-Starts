# /handlers/guides.py
from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.level4.guides_menu import get_guides_menu

router = Router()

@router.callback_query(F.data == "guides_menu")
async def guides_menu_handler(callback: CallbackQuery):
    """Обробник для меню Гайди"""
    await callback.message.edit_text(
        "📚 Гайди: Оберіть гайди:",
        reply_markup=get_guides_menu()
    )
