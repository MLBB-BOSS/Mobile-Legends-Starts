# UTC:21:40
# 2024-11-24
# keyboards/navigation_menu.py
# Author: MLBB-BOSS
# Description: Navigation menu keyboard layouts
# The era of artificial intelligence.

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_navigation_keyboard() -> ReplyKeyboardMarkup:
    """Підменю Навігація"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(
        KeyboardButton("🛡️ Персонажі"),
        KeyboardButton("📚 Гайди")
    )
    keyboard.row(
        KeyboardButton("⚖️ Контр-піки"),
        KeyboardButton("⚜️ Білди")
    )
    keyboard.row(
        KeyboardButton("📊 Голосування"),
        KeyboardButton("🔙 Назад до Головного")
    )
    return keyboard
