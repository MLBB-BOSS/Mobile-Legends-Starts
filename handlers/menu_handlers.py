from aiogram import Router
from aiogram.types import CallbackQuery

router = Router()

@router.callback_query(lambda c: c.data == "menu_navigation")
async def navigation_menu(callback: CallbackQuery):
    await callback.message.edit_text("🧭 Ви обрали Навігацію.")
