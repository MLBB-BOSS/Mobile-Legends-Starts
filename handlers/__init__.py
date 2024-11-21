# File: handlers/__init__.py

from .start_command import router as start_router
from .menu_handlers import router as menu_router
from .profile_handlers import router as profile_router
from .navigation_handlers import router as navigation_router

__all__ = [
    'start_router',
    'menu_router',
    'profile_router',
    'navigation_router'
]
