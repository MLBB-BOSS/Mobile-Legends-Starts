# keyboards/inline_menus.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_navigation_inline_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Перейти до Навігації", callback_data="go_navigation")],
        [InlineKeyboardButton(text="Дізнатися більше", callback_data="more_navigation")]
    ])

def get_profile_inline_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Перейти до Профілю", callback_data="go_profile")],
        [InlineKeyboardButton(text="Дізнатися більше", callback_data="more_profile")]
    ])
