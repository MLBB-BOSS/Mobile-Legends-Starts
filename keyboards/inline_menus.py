from typing import Final
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Constants
NEXT_BUTTON_TEXT: Final = "Далі ➡️"
START_BUTTON_TEXT: Final = "Розпочати 🚀"

def get_intro_page_1_keyboard() -> InlineKeyboardMarkup:
    """
    Get keyboard for intro page 1
    
    Returns:
        InlineKeyboardMarkup: Configured keyboard
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=NEXT_BUTTON_TEXT,
                    callback_data="intro_next_1"
                )
            ]
        ]
    )

def get_intro_page_2_keyboard() -> InlineKeyboardMarkup:
    """
    Get keyboard for intro page 2
    
    Returns:
        InlineKeyboardMarkup: Configured keyboard
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=NEXT_BUTTON_TEXT,
                    callback_data="intro_next_2"
                )
            ]
        ]
    )

def get_intro_page_3_keyboard() -> InlineKeyboardMarkup:
    """
    Get keyboard for intro page 3
    
    Returns:
        InlineKeyboardMarkup: Configured keyboard
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=START_BUTTON_TEXT,
                    callback_data="intro_start"
                )
            ]
        ]
    )
