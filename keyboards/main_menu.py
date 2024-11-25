# UTC:21:03
# 2024-11-25
# keyboards/main_menu.py
# Author: MLBB-BOSS
# Description: Main menu keyboard layouts
# The era of artificial intelligence.

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard() -> ReplyKeyboardMarkup:
    # Створюємо кнопки
    navigation_btn = KeyboardButton(text="🧭 Навігація")
    profile_btn = KeyboardButton(text="🪪 Профіль")
    
    # Створюємо клавіатуру та додаємо рядки з кнопками
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[navigation_btn, profile_btn]],  # Поміняли місцями кнопки
        resize_keyboard=True,
        input_field_placeholder="Виберіть опцію"
    )
    
    return keyboard
