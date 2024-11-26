# /handlers/heroes.py
from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.level3.heroes_menu import get_heroes_menu

router = Router()

@router.callback_query(F.data == "heroes_menu")
async def heroes_menu_handler(callback: CallbackQuery):
    """Обробник для меню Персонажі"""
    await callback.message.edit_text(
        "🛡️ Персонажі: Оберіть клас персонажів:",
        reply_markup=get_heroes_menu()
    )
