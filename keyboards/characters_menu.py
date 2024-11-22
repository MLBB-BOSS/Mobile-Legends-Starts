# keyboards/characters_menu.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_characters_menu() -> ReplyKeyboardMarkup:
    """
    Створює клавіатуру для розділу 'Персонажі'.
    
    Returns:
        ReplyKeyboardMarkup: Клавіатура для вибору персонажів.
    """
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🧙 Маги"), KeyboardButton(text="⚔️ Бійці")],
            [KeyboardButton(text="🛡️ Танки"), KeyboardButton(text="🏹 Стрільці")],
            [KeyboardButton(text="🔄 Назад до Головного Меню")],
        ],
        resize_keyboard=True
    )
