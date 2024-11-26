# /handlers/main_menu.py
from aiogram import Router
from aiogram.types import CallbackQuery
from keyboards.level1.main_menu import get_main_menu

router = Router()

@router.callback_query(lambda c: c.data == "main_menu")
async def main_menu_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        "Головне меню:",
        reply_markup=get_main_menu()
    )
