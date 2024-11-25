# UTC:22:00
# 2024-11-25
# handlers/__init__.py
# Author: MLBB-BOSS
# Description: Handlers module initialization
# The era of artificial intelligence.

from .main_menu import router as main_menu_router
from .navigation import router as navigation_router
from .user_handlers import router as user_handlers_router
from .profile_handlers import router as profile_handlers_router  # Import profile handlers

__all__ = [
    'main_menu_router',
    'navigation_router',
    'user_handlers_router',
    'profile_handlers_router'  # Add profile handlers to the exported module
]
