# /handlers/navigation.py
from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.level2.navigation_menu import get_navigation_menu

router = Router()

@router.callback_query(F.data == "navigation_menu")
async def navigation_menu_handler(callback: CallbackQuery):
    """Обробник для меню Навігація"""
    await callback.message.edit_text(
        "🧭 Навігація: Оберіть потрібний розділ:",
        reply_markup=get_navigation_menu()
    )
