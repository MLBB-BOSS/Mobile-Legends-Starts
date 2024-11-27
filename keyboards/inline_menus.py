# keyboards/inline_menus.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_navigation_inline_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Go to Navigation", callback_data="go_navigation")],
        [InlineKeyboardButton(text="Learn More", callback_data="more_navigation")]
    ])

def get_profile_inline_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Go to Profile", callback_data="go_profile")],
        [InlineKeyboardButton(text="Learn More", callback_data="more_profile")]
    ])
