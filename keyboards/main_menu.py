from aiogram import Router, F
from aiogram.types import Message
from keyboards.navigation_keyboard import NavigationKeyboard
from keyboards.keyboard_buttons import Buttons

router = Router()
nav_kb = NavigationKeyboard()

@router.message(F.text == str(Buttons.NAVIGATION))
async def handle_navigation_menu(message: Message):
    await message.answer("Оберіть опцію з меню навігації:", reply_markup=nav_kb.get_main_menu())
