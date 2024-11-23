import logging

logger = logging.getLogger(__name__)

try:
    from .main_menu import get_main_menu
    from .navigation_menu import get_navigation_menu
    from .hero_menu import get_hero_class_menu
    from .start_command import StartMenu
except ImportError as e:
    logger.error(f"Помилка імпорту: {e}")
    raise

__all__ = [
    "get_main_menu",
    "get_navigation_menu",
    "get_hero_class_menu",
    "StartMenu",
]
