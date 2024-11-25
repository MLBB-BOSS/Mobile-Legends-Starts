# UTC:21:40
# 2024-11-24
# keyboards/profile_menu.py
# Author: MLBB-BOSS
# Description: Profile menu keyboard layouts
# The era of artificial intelligence.

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_profile_keyboard() -> ReplyKeyboardMarkup:
    # Створюємо кнопки
    buttons = [
        [
            KeyboardButton(text="📈 Статистика"),
            KeyboardButton(text="🏆 Досягнення")
        ],
        [
            KeyboardButton(text="💌 Зворотний Зв'язок"),
            KeyboardButton(text="⚙️ Налаштування")
        ],
        [
            KeyboardButton(text="❓ Допомога"),
            KeyboardButton(text="🔙 Назад до Головного")
        ]
    ]
    
    # Створюємо клавіатуру
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder="Оберіть опцію профілю"
    )
    
    return keyboard
