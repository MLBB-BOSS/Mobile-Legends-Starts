# keyboards/__init__.py

from .start_command import StartMenu
from .menus import MainMenu
from .heroes_menu import HeroesMenu
from .help_menu import HelpMenu
from .profile_menu import ProfileMenu
# Додайте інші клавіатури тут

__all__ = [
    'StartMenu',
    'MainMenu',
    'HeroesMenu',
    'HelpMenu',
    'ProfileMenu',
    # Додайте інші клавіатури тут
]
