# File: handlers/menu_handler.py
from aiogram import Router, F, types
from aiogram.filters import Command
from keyboards import MainKeyboard, NavigationKeyboard, ProfileKeyboard
from utils.menu_states import MenuState
from utils.localization import loc

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    keyboard = MainKeyboard()
    await message.answer(
        text=loc.get_message("welcome"),
        reply_markup=keyboard.get_main_menu()
    )

@router.message(F.text == "🧭 Навігація")
async def navigation_menu(message: types.Message):
    keyboard = NavigationKeyboard()
    await message.answer(
        text=loc.get_message("navigation_menu"),
        reply_markup=keyboard.get_navigation_menu()
    )

# Add handlers for all menu items
