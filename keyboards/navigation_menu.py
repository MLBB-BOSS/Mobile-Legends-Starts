# UTC:21:32
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
