# handlers/__init__.py
# UTC:22:20
# 2024-11-25
# Author: MLBB-BOSS
# Description: Handlers initialization
# The era of artificial intelligence.

from .main_menu import router as main_menu_router
from .navigation import router as navigation_router
from .profile_handlers import router as profile_router
from .mp3_player import router as mp3_player_router  # Додано новий обробник для MP3 плеєра

__all__ = [
    'main_menu_router',
    'navigation_router',
    'profile_router',
    'mp3_player_router'  # Додано новий обробник для MP3 плеєра
]
