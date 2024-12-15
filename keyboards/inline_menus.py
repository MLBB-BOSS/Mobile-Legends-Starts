# keyboards/inline_menus.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """
    Створює головне меню з кнопкою 'Мій профіль'.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🪪 Мій Профіль", callback_data="my_profile")],
        [InlineKeyboardButton(text="🧭 Навігація", callback_data="navigation")]
    ])



def get_intro_page_1_keyboard() -> InlineKeyboardMarkup:
    """
    Створює інлайн-клавіатуру для першої сторінки вступу з кнопкою 'Далі'.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Далі", callback_data="intro_next_1")
        ]
    ])

def get_intro_page_2_keyboard() -> InlineKeyboardMarkup:
    """
    Створює інлайн-клавіатуру для другої сторінки вступу з кнопкою 'Далі'.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Далі", callback_data="intro_next_2")
        ]
    ])

def get_intro_page_3_keyboard() -> InlineKeyboardMarkup:
    """
    Створює інлайн-клавіатуру для третьої сторінки вступу з кнопкою 'Розпочати'.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Розпочати", callback_data="intro_start")
        ]
    ])

def get_generic_inline_keyboard() -> InlineKeyboardMarkup:
    """
    Створює інлайн-клавіатуру з однією кнопкою '---MLS---'.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="---MLS---", callback_data="mls_button")
        ]
    ])
