# handlers/__init__.py
# UTC:22:01
# 2024-11-25
# Author: MLBB-BOSS
# Description: Handlers initialization
# The era of artificial intelligence.

from .main_menu import router as main_menu_router
from .navigation import router as navigation_router
from .profile_menu import router as profile_router  # змінено з profile на profile_menu
from .characters_menu import router as characters_router  # змінено з characters на characters_menu

__all__ = [
    'main_menu_router',
    'navigation_router',
    'profile_router',
    'characters_router'
]
