# UTC:21:50
# 2024-11-24
# handlers/__init__.py
# Author: MLBB-BOSS
# Description: Handlers module initialization
# The era of artificial intelligence.

from .main_menu import router as main_menu_router
from .navigation import router as navigation_router
from .user_handlers import router as user_handlers_router

__all__ = [
    'main_menu_router',
    'navigation_router', 
    'user_handlers_router'
]
