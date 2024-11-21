# handlers/navigation_handlers.py
from aiogram import Router, F
from aiogram.types import Message
from keyboards.navigation_keyboard import NavigationKeyboard
from keyboards.keyboard_buttons import Buttons

router = Router()
kb = NavigationKeyboard()

@router.message(F.text == Buttons.NAVIGATION)
async def show_navigation_menu(message: Message):
    await message.answer(
        "Оберіть розділ навігації:",
        reply_markup=kb.get_navigation_menu()
    )

@router.message(F.text == Buttons.CHARACTERS)
async def show_characters_menu(message: Message):
    await message.answer(
        "Оберіть категорію героїв:",
        reply_markup=kb.get_characters_menu()
    )

@router.message(F.text == Buttons.MAPS)
async def show_maps_menu(message: Message):
    await message.answer(
        "Оберіть карту:",
        reply_markup=kb.get_maps_menu()
    )

@router.message(F.text == Buttons.TOURNAMENTS)
async def show_tournaments_menu(message: Message):
    await message.answer(
        "Оберіть турнір:",
        reply_markup=kb.get_tournaments_menu()
    )

@router.message(F.text == Buttons.GUIDES)
async def show_guides_menu(message: Message):
    await message.answer(
        "Оберіть гайд:",
        reply_markup=kb.get_guides_menu()
    )

@router.message(F.text == Buttons.BACK_TO_MAIN)
async def back_to_main_menu(message: Message):
    await message.answer(
        "Головне меню:",
        reply_markup=kb.get_main_menu()
    )
