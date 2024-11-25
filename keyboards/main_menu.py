# UTC:21:40
# 2024-11-24
# keyboards/main_menu.py
# Author: MLBB-BOSS
# Description: Main menu keyboard layouts
# The era of artificial intelligence.

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard() -> ReplyKeyboardMarkup:
    # Створюємо кнопки
    profile_btn = KeyboardButton(text="🪪 Профіль")
    navigation_btn = KeyboardButton(text="🧭 Навігація")
    
    # Створюємо клавіатуру та додаємо рядки з кнопками
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[profile_btn, navigation_btn]],  # Розміщуємо кнопки в одному рядку
        resize_keyboard=True,
        input_field_placeholder="Виберіть опцію"
    )
    
    return keyboard
