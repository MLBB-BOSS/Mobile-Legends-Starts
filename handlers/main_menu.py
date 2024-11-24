# handlers/menu_handlers.py
# Created: 2024-11-24
# Author: MLBB-BOSS
# Description: Обробники для меню навігації та профілю

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.filters import Command

from keyboards.menu_keyboards import NavigationKeyboards, ProfileKeyboards

router = Router()

# Обробники для навігації
@router.callback_query(F.data == "nav_main")
async def show_navigation_menu(callback: CallbackQuery):
    """Показує головне меню навігації"""
    await callback.message.edit_text(
        "🧭 Оберіть розділ навігації:",
        reply_markup=NavigationKeyboards.main_navigation()
    )

@router.callback_query(F.data == "nav_heroes")
async def show_heroes_menu(callback: CallbackQuery):
    """Показує меню вибору героїв"""
    await callback.message.edit_text(
        "🛡️ Оберіть клас героя або скористайтесь пошуком:",
        reply_markup=NavigationKeyboards.heroes_submenu()
    )

# Обробники для профілю
@router.callback_query(F.data == "profile_main")
async def show_profile_menu(callback: CallbackQuery):
    """Показує головне меню профілю"""
    await callback.message.edit_text(
        "🪪 Ваш профіль - оберіть розділ:",
        reply_markup=ProfileKeyboards.main_profile()
    )

@router.callback_query(F.data == "profile_stats")
async def show_stats_menu(callback: CallbackQuery):
    """Показує меню статистики"""
    await callback.message.edit_text(
        "📈 Оберіть тип статистики для перегляду:",
        reply_markup=ProfileKeyboards.stats_submenu()
    )

@router.callback_query(F.data == "profile_settings")
async def show_settings_menu(callback: CallbackQuery):
    """Показує меню налаштувань"""
    await callback.message.edit_text(
        "⚙️ Налаштування профілю:",
        reply_markup=ProfileKeyboards.settings_submenu()
    )

# Повернення до головного меню
@router.callback_query(F.data == "main_menu")
async def return_to_main_menu(callback: CallbackQuery):
    """Повертає до головного меню"""
    from keyboards.main_keyboard import get_main_keyboard  # Імпортуємо головну клавіатуру
    await callback.message.edit_text(
        "🏠 Головне меню:",
        reply_markup=get_main_keyboard()
    )
