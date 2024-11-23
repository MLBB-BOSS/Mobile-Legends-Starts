# handlers/__init__.py

from .menu import menu_router
from .navigation import navigation_router
from .heroes import hero_router

__all__ = [
    "menu_router",
    "navigation_router",
    "hero_router",
]
