# keyboards/hero_menu.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_hero_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Герой 1"), KeyboardButton(text="Герой 2")],
            [KeyboardButton(text="Назад")],
        ],
        resize_keyboard=True
    )
