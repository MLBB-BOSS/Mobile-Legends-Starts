# utils/keyboards.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """Створює клавіатуру головного меню"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(text="🏆 Турніри", callback_data="tournaments"),
        InlineKeyboardButton(text="👤 Профіль", callback_data="profile"),
        InlineKeyboardButton(text="📊 Статистика", callback_data="stats"),
        InlineKeyboardButton(text="ℹ️ Довідка", callback_data="help")
    )
    return keyboard

def get_profile_keyboard() -> InlineKeyboardMarkup:
    """Створює клавіатуру для профілю"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(text="📊 Статистика", callback_data="profile_stats"),
        InlineKeyboardButton(text="🏆 Досягнення", callback_data="profile_achievements"),
        InlineKeyboardButton(text="📝 Редагувати", callback_data="profile_edit"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="menu_main")
    )
    return keyboard
