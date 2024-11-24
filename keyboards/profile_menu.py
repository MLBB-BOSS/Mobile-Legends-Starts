# UTC:21:40
# 2024-11-24
# keyboards/profile_menu.py
# Author: MLBB-BOSS
# Description: Profile menu keyboard layouts
# The era of artificial intelligence.

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_profile_keyboard() -> ReplyKeyboardMarkup:
    """Підменю Профіль"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(
        KeyboardButton("📈 Статистика"),
        KeyboardButton("🏆 Досягнення")
    )
    keyboard.row(
        KeyboardButton("⚙️ Налаштування"),
        KeyboardButton("💌 Зворотний Зв'язок")
    )
    keyboard.row(
        KeyboardButton("❓ Допомога"),
        KeyboardButton("🔙 Назад до Головного")
    )
    return keyboard
