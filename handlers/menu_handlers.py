from aiogram import Router, F
from aiogram.types import Message
from keyboards import MenuKeyboard, Buttons
import logging

logger = logging.getLogger(__name__)
router = Router()
kb = MenuKeyboard()

@router.message(F.text == "🧭 Навігація")
async def show_navigation(message: Message):
    await message.answer(
        "Меню навігації:",
        reply_markup=kb.get_navigation_menu()
    )

@router.message(F.text == "🎯 Герої")
async def show_heroes(message: Message):
    await message.answer(
        "Оберіть клас героя:",
        reply_markup=kb.get_heroes_menu()
    )

@router.message(F.text == "🏆 Турніри")
async def show_tournaments(message: Message):
    await message.answer(
        "Меню турнірів:",
        reply_markup=kb.get_tournaments_menu()
    )

@router.message(F.text == "👤 Профіль")
async def show_profile(message: Message):
    await message.answer(
        "Ваш профіль:",
        reply_markup=kb.get_profile_menu()
    )

@router.message(F.text == "⚙️ Налаштування")
async def show_settings(message: Message):
    await message.answer(
        "Налаштування:",
        reply_markup=kb.get_settings_menu()
    )

@router.message(F.text == "🏠 Головне меню")
async def show_main_menu(message: Message):
    await message.answer(
        "Головне меню:",
        reply_markup=kb.get_main_menu()
    )

@router.message(F.text == "🔙 Назад")
async def handle_back(message: Message):
    # В залежності від поточного рівня меню повертаємося на рівень вище
    if kb._current_level == MenuLevel.NAVIGATION:
        await show_main_menu(message)
    elif kb._current_level == MenuLevel.HEROES:
        await show_main_menu(message)
    elif kb._current_level == MenuLevel.TOURNAMENTS:
        await show_main_menu(message)
    elif kb._current_level == MenuLevel.PROFILE:
        await show_main_menu(message)
    elif kb._current_level == MenuLevel.SETTINGS:
        await show_main_menu(message)
    else:
        await show_main_menu(message)
