from aiogram import Router, F, types  # Додано 'types'
from aiogram.types import CallbackQuery
from keyboards import NavigationMenu, ProfileMenu, MainMenu
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery):
    keyboard = MainMenu.get_main_menu()
    await callback.message.edit_reply_markup(reply_markup=keyboard)
    await callback.answer()

@router.message(F.text == "🧭 Навігація")
async def show_navigation(message: types.Message):  # 'types' виправлено
    keyboard = NavigationMenu.get_navigation_menu()
    await message.answer("Оберіть розділ навігації:", reply_markup=keyboard)
