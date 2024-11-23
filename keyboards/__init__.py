# keyboards/__init__.py

from .menu import menu_router
from .navigation import navigation_router
from .hero_class_handlers import hero_class_router  # Оновлено назву імпорту

__all__ = [
    "menu_router",
    "navigation_router",
    "hero_class_router",  # Оновлено відповідно до правильного роутера
]
