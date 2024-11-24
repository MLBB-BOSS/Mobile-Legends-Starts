# UTC:21:48
# 2024-11-24
# keyboards/__init__.py
# Author: MLBB-BOSS
# Description: Keyboards module initialization
# The era of artificial intelligence.

from .main_menu import get_main_keyboard
from .navigation_menu import get_navigation_keyboard
from .profile_menu import get_profile_keyboard

__all__ = [
    'get_main_keyboard',
    'get_navigation_keyboard',
    'get_profile_keyboard'
]
