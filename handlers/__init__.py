# handlers/__init__.py
# UTC:22:10
# 2024-11-25
# Author: MLBB-BOSS
# Description: Handlers initialization
# The era of artificial intelligence.

from .main_menu import router as main_menu_router
from .navigation import router as navigation_router
# Змінюємо імпорт на існуючий файл
from .profile_handlers import router as profile_router
from .characters_menu import router as characters_router

__all__ = [
    'main_menu_router',
    'navigation_router',
    'profile_router',
    'characters_router'
]
