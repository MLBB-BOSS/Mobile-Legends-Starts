from typing import Final
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Constants
NEXT_BUTTON_TEXT: Final = "Далі ➡️"
START_BUTTON_TEXT: Final = "Розпочати 🚀"


def get_intro_page_1_keyboard() -> InlineKeyboardMarkup:
    """
    Клавіатура для сторінки 1 інтро.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=NEXT_BUTTON_TEXT, callback_data="intro_next_1")]
        ]
    )


def get_intro_page_2_keyboard() -> InlineKeyboardMarkup:
    """
    Клавіатура для сторінки 2 інтро.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=NEXT_BUTTON_TEXT, callback_data="intro_next_2")]
        ]
    )


def get_intro_page_3_keyboard() -> InlineKeyboardMarkup:
    """
    Клавіатура для сторінки 3 інтро.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=START_BUTTON_TEXT, callback_data="intro_start")]
        ]
    )
