# /keyboards/level1/main_menu.py
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_main_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="🧭 Навігація", callback_data="navigation_menu")
    builder.button(text="🪪 Профіль", callback_data="profile_menu")
    builder.adjust(2)
    return builder.as_markup()
