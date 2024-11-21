# handlers/navigation_handlers.py
from aiogram import Router, F
from aiogram.types import Message
from keyboards.navigation_keyboard import NavigationKeyboard
from keyboards.keyboard_buttons import Buttons

router = Router()
nav_kb = NavigationKeyboard()

@router.message(F.text == Buttons.NAVIGATION)
async def show_navigation(message: Message):
    await message.answer(
        "Оберіть розділ:",
        reply_markup=nav_kb.get_navigation_menu()
    )

@router.message(F.text == Buttons.MAIN_MENU)
async def show_main_menu(message: Message):
    await message.answer(
        "Головне меню:",
        reply_markup=nav_kb.get_main_menu()
    )
