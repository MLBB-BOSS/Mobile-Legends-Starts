# UTC:21:40
# 2024-11-24
# keyboards/navigation_menu.py
# Author: MLBB-BOSS
# Description: Navigation menu keyboard layouts
# The era of artificial intelligence.

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_navigation_keyboard() -> ReplyKeyboardMarkup:
    # Створюємо кнопки
    buttons = [
        [
            KeyboardButton(text="🛡️ Персонажі"),
            KeyboardButton(text="📚 Гайди")
        ],
        [
            KeyboardButton(text="⚖️ Контр-піки"),
            KeyboardButton(text="⚜️ Білди")
        ],
        [
            KeyboardButton(text="📊 Голосування"),
            KeyboardButton(text="❓ Допомога")
        ],
        [
            KeyboardButton(text="🔙 Назад до Головного")
        ]
    ]
    
    # Створюємо клавіатуру
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder="Оберіть розділ"
    )
    
    return keyboard
