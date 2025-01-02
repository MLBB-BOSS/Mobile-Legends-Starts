# keyboards/helpers.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """
    Створює клавіатуру головного меню.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Профіль", callback_data="menu_profile")],
            [InlineKeyboardButton(text="Статистика", callback_data="menu_stats")],
            [InlineKeyboardButton(text="Команда", callback_data="menu_team")],
            [InlineKeyboardButton(text="Турніри", callback_data="menu_tournament")],
        ]
    )
