# keyboards/__init__.py
from .main_menu import get_main_keyboard
from .profile_menu import get_profile_keyboard

__all__ = [
    'get_main_keyboard',
    'get_profile_keyboard'
]
