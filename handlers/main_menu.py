# handlers/main_menu.py
# Created: 2024-11-24
# Author: MLBB-BOSS
# Description: Обробники для меню навігації та профілю

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from keyboards.main_menu import NavigationKeyboards, ProfileKeyboards

router = Router()

# Обробники для навігації
@router.message(Command("navigation"))
async def show_navigation_menu(message: Message):
    """
    Показує головне меню навігації
    """
    await message.answer(
        "🧭 Оберіть розділ навігації:",
        reply_markup=NavigationKeyboards.main_navigation()
    )

@router.message(Command("heroes"))
async def show_heroes_menu(message: Message):
    """
    Показує меню вибору героїв
    """
    await message.answer(
        "🛡️ Оберіть клас героя або скористайтесь пошуком:",
        reply_markup=NavigationKeyboards.heroes_submenu()
    )

# Обробники для профілю
@router.message(Command("profile"))
async def show_profile_menu(message: Message):
    """
    Показує головне меню профілю
    """
    await message.answer(
        "🪪 Ваш профіль - оберіть розділ:",
        reply_markup=ProfileKeyboards.main_profile()
    )

@router.message(Command("stats"))
async def show_stats_menu(message: Message):
    """
    Показує меню статистики
    """
    await message.answer(
        "📈 Оберіть тип статистики для перегляду:",
        reply_markup=ProfileKeyboards.stats_submenu()
    )

@router.message(Command("settings"))
async def show_settings_menu(message: Message):
    """
    Показує меню налаштувань
    """
    await message.answer(
        "⚙️ Налаштування профілю:",
        reply_markup=ProfileKeyboards.settings_submenu()
    )

# Повернення до головного меню
@router.message(Command("main_menu"))
async def return_to_main_menu(message: Message):
    """
    Повертає до головного меню
    """
    from keyboards.main_keyboard import get_main_keyboard  # Імпортуємо головну клавіатуру
    await message.answer(
        "🏠 Головне меню:",
        reply_markup=get_main_keyboard()
    )
