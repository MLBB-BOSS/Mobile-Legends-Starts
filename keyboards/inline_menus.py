# keyboards/inline_menus.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_generic_inline_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    return keyboard

def get_intro_page_1_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Далі", callback_data="intro_next_1")],
        ]
    )
    return keyboard

def get_intro_page_2_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Далі", callback_data="intro_next_2")],
        ]
    )
    return keyboard

def get_intro_page_3_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Розпочати", callback_data="intro_start")],
        ]
    )
    return keyboard
