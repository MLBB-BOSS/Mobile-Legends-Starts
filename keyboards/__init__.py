# UTC:22:06
# 2024-11-24
# keyboards/__init__.py
# Author: MLBB-BOSS
# Description: Keyboards module initialization
# The era of artificial intelligence.

from .main_menu import get_main_keyboard as main_menu_keyboard
from .navigation_menu import get_navigation_keyboard as navigation_keyboard
from .profile_menu import get_profile_keyboard as profile_keyboard

__all__ = [
    'main_menu_keyboard',
    'navigation_keyboard', 
    'profile_keyboard'
]
