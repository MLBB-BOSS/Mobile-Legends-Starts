# keyboards/navigation_menu.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_navigation_menu():
    """
    Повертає клавіатуру для розділу «Навігація».
    """
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛡️ Персонажі"), KeyboardButton(text="📚 Гайди")],
            [KeyboardButton(text="⚖️ Контр-піки"), KeyboardButton(text="⚜️ Білди")],
            [KeyboardButton(text="🔄 Повернутися до Головного Меню")]
        ],
        resize_keyboard=True
    )
