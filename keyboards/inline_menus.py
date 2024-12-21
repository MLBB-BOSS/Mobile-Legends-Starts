# keyboards/inline_menus.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_generic_inline_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Назад до меню", callback_data="menu_back")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_intro_page_1_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Далі", callback_data="intro_next_1")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_intro_page_2_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Далі", callback_data="intro_next_2")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_intro_page_3_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Почати", callback_data="intro_start")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Define other inline keyboards as needed