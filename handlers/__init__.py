from .start_command import router as start_router
from .menu_handlers import router as menu_router
from .message_handlers import router as message_router
from .error_handler import router as error_router
from .hero_class_handlers import router as hero_class_router
from .hero_handlers import router as hero_router
from .navigation_handlers import router as navigation_router

__all__ = [
    "start_router",
    "menu_router",
    "message_router",
    "error_router",
    "hero_class_router",
    "hero_router",
    "navigation_router"
]
