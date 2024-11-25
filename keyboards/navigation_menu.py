# UTC:21:40
# 2024-11-24
# keyboards/navigation_menu.py
# Author: MLBB-BOSS
# Description: Navigation menu keyboard layouts
# The era of artificial intelligence.
# keyboards/navigation_menu.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_navigation_keyboard() -> ReplyKeyboardMarkup:
    """Підменю Навігація"""
    keyboard = ReplyKeyboardMarkup(
        rows=[
            [KeyboardButton(text="🛡️ Персонажі"), KeyboardButton(text="📚 Гайди")],
            [KeyboardButton(text="⚖️ Контр-піки"), KeyboardButton(text="⚜️ Білди")],
            [KeyboardButton(text="📊 Голосування"), KeyboardButton(text="🔙 Назад до Головного")]
        ],
        resize_keyboard=True
    )
    return keyboard
