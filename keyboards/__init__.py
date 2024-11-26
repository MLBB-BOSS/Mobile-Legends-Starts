# keyboards/__init__.py

from .main_menu import (
    get_main_keyboard,
    get_profile_keyboard,
    get_navigation_keyboard,
    get_characters_keyboard  # Імпортуємо get_characters_keyboard з main_menu.py
)
from .mp3_player_menu import get_mp3_player_keyboard

__all__ = [
    'get_main_keyboard',
    'get_profile_keyboard',
    'get_navigation_keyboard',
    'get_characters_keyboard',
    'get_mp3_player_keyboard'
]
