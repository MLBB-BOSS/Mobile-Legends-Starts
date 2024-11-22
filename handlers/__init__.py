# handlers/__init__.py

from .router import router
from .start_command import start_router
from .menu_handlers import menu_router
from .navigation_handlers import navigation_router
from .profile_handlers import profile_router

__all__ = [
    "router",
    "start_router",
    "menu_router",
    "navigation_router",
    "profile_router",
]
