# UTC:21:40
# 2024-11-24
# keyboards/navigation_menu.py
# Author: MLBB-BOSS
# Description: Navigation menu keyboard layouts
# The era of artificial intelligence.
# keyboards/navigation_menu.py
# keyboards/navigation_menu.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_navigation_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        KeyboardButton("🛡️ Персонажі"),
        KeyboardButton("📚 Гайди"),
        KeyboardButton("⚖️ Контр-піки"),
        KeyboardButton("⚜️ Білди"),
        KeyboardButton("📊 Голосування"),
        KeyboardButton("🔙 Назад")
    ]
    keyboard.add(*buttons)
    return keyboard
