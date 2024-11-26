# /handlers/navigation.py
from aiogram import Router
from aiogram.types import CallbackQuery
from keyboards.level2.navigation_menu import get_navigation_menu

router = Router()

@router.callback_query(lambda c: c.data == "navigation_menu")
async def navigation_menu_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        "🧭 Навігація: Оберіть потрібний розділ:",
        reply_markup=get_navigation_menu()
    )
