# UTC:21:40
# 2024-11-24
# keyboards/profile_menu.py
# Author: MLBB-BOSS
# Description: Profile menu keyboard layouts
# The era of artificial intelligence.

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_profile_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        KeyboardButton("🔙 Назад"),
        # Додайте інші кнопки за потреби
    ]
    keyboard.add(*buttons)
    return keyboard
