from aiogram import Router, F
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
async def show_navigation(message: types.Message):
    keyboard = NavigationMenu.get_navigation_menu()
    await message.answer("Оберіть розділ навігації:", reply_markup=keyboard)

@router.message(F.text == "🪧 Мій Кабінет")
async def show_profile(message: types.Message):
    keyboard = ProfileMenu.get_profile_menu()
    await message.answer("Ваш особистий кабінет:", reply_markup=keyboard)
