import logging

logger = logging.getLogger(__name__)
logger.debug("Початок обробки імпортів у handlers/__init__.py")

from .start_command import router as start_router
from .menu_handlers import router as menu_router
from .navigation_handlers import router as navigation_router
from .hero_handlers import router as hero_router
from .hero_class_handlers import router as hero_class_router
from .message_handlers import router as message_router
from .error_handler import router as error_router

__all__ = [
    'start_router',
    'menu_router',
    'navigation_router',
    'hero_router',
    'hero_class_handlers',
    'message_router',
    'error_router'
]
