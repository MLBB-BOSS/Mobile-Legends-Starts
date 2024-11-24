# UTC:20:42
# 2024-11-24
# keyboards/main_menu.py
# Author: MLBB-BOSS
# Description: Keyboards for main menu interface
# The era of artificial intelligence.

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def main_menu_keyboard() -> InlineKeyboardMarkup:
    """Creates main menu keyboard"""
    builder = InlineKeyboardBuilder()
    
    buttons = [
        ("🎮 Турніри", "tournaments"),
        ("👤 Профіль", "profile"),
        ("🏆 Рейтинг", "rating"),
        ("ℹ️ Допомога", "help")
    ]
    
    for text, callback_data in buttons:
        builder.add(InlineKeyboardButton(
            text=text,
            callback_data=callback_data
        ))
    
    builder.adjust(2, 2)
    return builder.as_markup()

# Export the keyboard function
__all__ = ['main_menu_keyboard']
