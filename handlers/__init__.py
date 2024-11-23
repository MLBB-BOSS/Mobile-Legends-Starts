from .menu import menu_router
from .navigation import navigation_router
from .heroes import heroes_router  # Додати цей імпорт

__all__ = [
    "menu_router",
    "navigation_router",
    "hero_router",
]
