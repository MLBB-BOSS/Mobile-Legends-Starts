# keyboards/builds_menu.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_builds_menu() -> ReplyKeyboardMarkup:
    """
    Створює клавіатуру для розділу 'Білди'.
    
    Returns:
        ReplyKeyboardMarkup: Клавіатура з кнопками для білдів.
    """
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛠️ Огляд Білдів"), KeyboardButton(text="📜 Історія Білдів")],
            [KeyboardButton(text="🔄 Назад до Головного Меню")],
        ],
        resize_keyboard=True
    )
