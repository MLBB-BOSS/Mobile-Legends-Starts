# handlers/menu_handlers.py
from aiogram import Router, F
from aiogram.types import Message
from keyboards.menu_keyboard import MenuKeyboard
from keyboards.keyboard_buttons import Buttons, MenuLevel

router = Router()
kb = MenuKeyboard()

@router.message(F.text == Buttons.MAIN_MENU)
async def show_main_menu(message: Message):
    await message.answer(
        "Головне меню:",
        reply_markup=kb.get_main_menu()
    )

@router.message(F.text == Buttons.NAVIGATION)
async def show_navigation(message: Message):
    await message.answer(
        "Меню навігації:",
        reply_markup=kb.get_navigation_menu()
    )

@router.message(F.text == Buttons.HEROES)
async def show_heroes(message: Message):
    await message.answer(
        "Оберіть клас героя:",
        reply_markup=kb.get_heroes_menu()
    )

@router.message(F.text == Buttons.TOURNAMENTS)
async def show_tournaments(message: Message):
    await message.answer(
        "Меню турнірів:",
        reply_markup=kb.get_tournaments_menu()
    )

@router.message(F.text == Buttons.PROFILE)
async def show_profile(message: Message):
    await message.answer(
        "Ваш профіль:",
        reply_markup=kb.get_profile_menu()
    )

@router.message(F.text == Buttons.BACK)
async def handle_back(message: Message):
    if kb._current_level == MenuLevel.NAVIGATION:
        await show_main_menu(message)
    elif kb._current_level == MenuLevel.HEROES:
        await show_main_menu(message)
    # і так далі для інших рівнів
