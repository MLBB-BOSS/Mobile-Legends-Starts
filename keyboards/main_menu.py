# keyboards/main_menu.py
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from typing import List

def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    """
    Create main menu keyboard
    
    Returns:
        ReplyKeyboardMarkup: Main menu keyboard
    """
    keyboard = [
        [
            KeyboardButton(text="🧭 Навігація"),
            KeyboardButton(text="🪪 Профіль")
        ],
        [
            KeyboardButton(text="⚔️ Герої"),
            KeyboardButton(text="🏆 Турніри")
        ],
        [
            KeyboardButton(text="📚 Гайди"),
            KeyboardButton(text="⚡️ Буст")
        ]
    ]
    
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder="Оберіть опцію з меню"
    )

def get_main_menu_inline_keyboard() -> InlineKeyboardMarkup:
    """
    Create main menu inline keyboard
    
    Returns:
        InlineKeyboardMarkup: Main menu inline keyboard
    """
    keyboard = [
        [
            InlineKeyboardButton(
                text="🧭 Навігація",
                callback_data="nav_main"
            ),
            InlineKeyboardButton(
                text="🪪 Профіль",
                callback_data="profile_main"
            )
        ],
        [
            InlineKeyboardButton(
                text="⚔️ Герої",
                callback_data="heroes_main"
            ),
            InlineKeyboardButton(
                text="🏆 Турніри",
                callback_data="tournaments_main"
            )
        ],
        [
            InlineKeyboardButton(
                text="📚 Гайди",
                callback_data="guides_main"
            ),
            InlineKeyboardButton(
                text="⚡️ Буст",
                callback_data="boost_main"
            )
        ]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# Constants for callback data
class MainMenuCallbacks:
    """Main menu callback data"""
    NAVIGATION = "nav_main"
    PROFILE = "profile_main"
    HEROES = "heroes_main"
    TOURNAMENTS = "tournaments_main"
    GUIDES = "guides_main"
    BOOST = "boost_main"

# Button text constants
class MainMenuButtons:
    """Main menu button texts"""
    NAVIGATION = "🧭 Навігація"
    PROFILE = "🪪 Профіль"
    HEROES = "⚔️ Герої"
    TOURNAMENTS = "🏆 Турніри"
    GUIDES = "📚 Гайди"
    BOOST = "⚡️ Буст"

def create_keyboard_row(buttons: List[str]) -> List[KeyboardButton]:
    """
    Create keyboard row from button texts
    
    Args:
        buttons: List of button texts
        
    Returns:
        List[KeyboardButton]: List of keyboard buttons
    """
    return [KeyboardButton(text=text) for text in buttons]
