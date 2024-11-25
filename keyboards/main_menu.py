# UTC:21:40
# 2024-11-24
# keyboards/main_menu.py
# Author: MLBB-BOSS
# Description: Main menu keyboard layouts
# The era of artificial intelligence.

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Головне меню"""
    keyboard = ReplyKeyboardMarkup(keyboard=[], resize_keyboard=True)
    keyboard.row(
        KeyboardButton("🧭 Навігація"),
        KeyboardButton("🪪 Профіль")
    )
    return keyboard
