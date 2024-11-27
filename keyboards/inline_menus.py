# keyboards/inline_menus.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_generic_inline_keyboard():
    inline_keyboard = [
        [
            InlineKeyboardButton(text="Button 1", callback_data="button1"),
            InlineKeyboardButton(text="Button 2", callback_data="button2")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
