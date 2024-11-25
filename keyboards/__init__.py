# keyboards/__init__.py
# UTC:21:56
# 2024-11-25
# Author: MLBB-BOSS
# Description: Keyboards initialization
# The era of artificial intelligence.

from .main_menu import get_main_keyboard
from .profile_menu import get_profile_keyboard
from .navigation_menu import (
    get_navigation_keyboard,
    get_characters_keyboard,
    get_guides_keyboard,
    get_counterpicks_keyboard,
    get_builds_keyboard,
    get_voting_keyboard,
    get_help_keyboard
)

__all__ = [
    'get_main_keyboard',
    'get_profile_keyboard',
    'get_navigation_keyboard',
    'get_characters_keyboard',
    'get_guides_keyboard',
    'get_counterpicks_keyboard',
    'get_builds_keyboard',
    'get_voting_keyboard',
    'get_help_keyboard'
]
