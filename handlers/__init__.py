# handlers/__init__.py
# UTC:21:56
# 2024-11-25
# Author: MLBB-BOSS
# Description: Handlers initialization
# The era of artificial intelligence.

from .main_menu import router as main_menu_router
from .navigation import router as navigation_router
from .profile import router as profile_router
from .characters import router as characters_router
from .guides import router as guides_router
from .counterpicks import router as counterpicks_router
from .builds import router as builds_router
from .voting import router as voting_router
from .help import router as help_router

__all__ = [
    'main_menu_router',
    'navigation_router',
    'profile_router',
    'characters_router',
    'guides_router',
    'counterpicks_router',
    'builds_router',
    'voting_router',
    'help_router'
]
