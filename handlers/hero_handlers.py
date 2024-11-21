# handlers/hero_handlers.py
from aiogram import Router, F
from aiogram.types import Message
from keyboards.navigation_keyboard import NavigationKeyboard
from keyboards.keyboard_buttons import Buttons

router = Router()
kb = NavigationKeyboard()

@router.message(F.text == Buttons.HEROES)
async def show_heroes_menu(message: Message):
    await message.answer(
        "Оберіть категорію героїв:",
        reply_markup=kb.get_navigation_menu()
    )

@router.message(F.text == Buttons.CHARACTERS)
async def show_characters(message: Message):
    await message.answer(
        "Оберіть героя:",
        reply_markup=kb.get_navigation_menu()
    )
