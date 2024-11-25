# keyboards/__init__.py
# UTC:22:03
# 2024-11-25
# Author: MLBB-BOSS
# Description: Keyboards initialization
# The era of artificial intelligence.

from .main_menu import get_main_keyboard
from .profile_menu import get_profile_keyboard
from .navigation_menu import get_navigation_keyboard
from .characters_menu import get_characters_keyboard
from .mp3_player_menu import get_mp3_player_keyboard  # Додано нову клавіатуру для MP3 плеєра

__all__ = [
    'get_main_keyboard',
    'get_profile_keyboard',
    'get_navigation_keyboard',
    'get_characters_keyboard',
    'get_mp3_player_keyboard'  # Додано нову клавіатуру для MP3 плеєра
]
