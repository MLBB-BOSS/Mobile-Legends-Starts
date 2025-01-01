from typing import List, Dict, Union
from enum import Enum, auto
from dataclasses import dataclass
from aiogram.types import (
    ReplyKeyboardMarkup, 
    KeyboardButton, 
    InlineKeyboardMarkup, 
    InlineKeyboardButton
)
from logging import getLogger

logger = getLogger(__name__)

class MenuCallbackData(str, Enum):
    """Callback data for menu buttons"""
    NAVIGATION = "navigation"
    PROFILE = "profile"
    BACK = "back"

@dataclass
class MenuButton:
    """Menu button configuration"""
    text: str
    callback_data: str

class MainMenuButtons:
    """Main menu button configurations"""
    NAVIGATION = MenuButton("🧭 Навігація", MenuCallbackData.NAVIGATION)
    PROFILE = MenuButton("🪪 Мій Профіль", MenuCallbackData.PROFILE)
    BACK = MenuButton("🔙 Назад", MenuCallbackData.BACK)

def create_inline_keyboard(
    buttons: List[MenuButton],
    row_width: int = 2
) -> InlineKeyboardMarkup:
    """
    Create inline keyboard from buttons
    
    Args:
        buttons: List of MenuButton objects
        row_width: Number of buttons per row
        
    Returns:
        InlineKeyboardMarkup: Configured inline keyboard
    """
    keyboard = []
    for i in range(0, len(buttons), row_width):
        row = [
            InlineKeyboardButton(
                text=btn.text,
                callback_data=btn.callback_data
            ) for btn in buttons[i:i + row_width]
        ]
        keyboard.append(row)
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_main_menu_inline() -> InlineKeyboardMarkup:
    """
    Get main menu inline keyboard
    
    Returns:
        InlineKeyboardMarkup: Main menu keyboard
    """
    buttons = [
        MainMenuButtons.NAVIGATION,
        MainMenuButtons.PROFILE
    ]
    return create_inline_keyboard(buttons)

def create_reply_keyboard(
    buttons: List[str],
    row_width: int = 2,
    resize_keyboard: bool = True,
    placeholder: str | None = None
) -> ReplyKeyboardMarkup:
    """
    Create reply keyboard from button texts
    
    Args:
        buttons: List of button texts
        row_width: Number of buttons per row
        resize_keyboard: Whether to resize keyboard
        placeholder: Input field placeholder
        
    Returns:
        ReplyKeyboardMarkup: Configured reply keyboard
    """
    keyboard = []
    for i in range(0, len(buttons), row_width):
        row = [KeyboardButton(text=text) for text in buttons[i:i + row_width]]
        keyboard.append(row)
        
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=resize_keyboard,
        input_field_placeholder=placeholder
    )

def get_main_menu() -> ReplyKeyboardMarkup:
    """
    Get main menu reply keyboard
    
    Returns:
        ReplyKeyboardMarkup: Main menu keyboard
    """
    buttons = [
        MainMenuButtons.NAVIGATION.text,
        MainMenuButtons.PROFILE.text
    ]
    return create_reply_keyboard(
        buttons=buttons,
        placeholder="Оберіть одну з основних опцій"
    )
