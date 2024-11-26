# /handlers/main_menu.py
from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.level1.main_menu import get_main_menu

router = Router()

@router.callback_query(F.data == "main_menu")
async def main_menu_handler(callback: CallbackQuery):
    """Повернення до головного меню"""
    await callback.message.edit_text(
        "Головне меню. Оберіть опцію:",
        reply_markup=get_main_menu()
    )
