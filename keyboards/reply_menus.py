# keyboards/reply_menus.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_reply_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        KeyboardButton(text="Опція 1"),
        KeyboardButton(text="Опція 2"),
        KeyboardButton(text="Опція 3")
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[buttons],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard
