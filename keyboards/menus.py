# keyboards/menus.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Навігація"), KeyboardButton(text="Мій профіль")]
        ],
        resize_keyboard=True
    )
