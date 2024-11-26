# /handlers/heroes.py
from aiogram import Router
from aiogram.types import CallbackQuery
from keyboards.level3.heroes_menu import get_heroes_menu

router = Router()

@router.callback_query(lambda c: c.data == "heroes_menu")
async def heroes_menu_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        "🛡️ Персонажі: Оберіть клас:",
        reply_markup=get_heroes_menu()
    )
