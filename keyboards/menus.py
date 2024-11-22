# keyboards/menus.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_menu():
    """
    Повертає головну клавіатуру бота з кнопками.
    """
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Навігація"), KeyboardButton(text="Мій профіль")]
        ],
        resize_keyboard=True
    )
