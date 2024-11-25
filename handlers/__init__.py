# handlers/__init__.py
from .main_menu import router as main_menu_router
from .navigation import router as navigation_router
from .profile import router as profile_handlers_router  # Змініть імпорт на .profile

__all__ = [
    'main_menu_router',
    'navigation_router',
    'profile_handlers_router'
]
