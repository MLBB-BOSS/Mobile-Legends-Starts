# keyboards/__init__.py
from .main_menu import get_main_keyboard
from .profile_menu import get_profile_keyboard
from .navigation_menu import get_navigation_keyboard  # Додано, якщо існує

__all__ = [
    'get_main_keyboard',
    'get_profile_keyboard',
    'get_navigation_keyboard'  # Додано, якщо існує
]
