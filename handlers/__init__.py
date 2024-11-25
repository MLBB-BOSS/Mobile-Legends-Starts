# UTC:22:00
# 2024-11-25
# handlers/__init__.py
# Author: MLBB-BOSS
# Description: Handlers module initialization
# The era of artificial intelligence.

from .main_menu import router as main_menu_router
from .navigation import router as navigation_router
from .profile_handlers import router as profile_handlers_router  # Додано профільні хендлери

__all__ = [
    'main_menu_router',
    'navigation_router',
    'profile_handlers_router'  # Видалено user_handlers_router
]
