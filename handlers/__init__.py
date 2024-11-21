# handlers/__init__.py

from .start_command import router as start_router
from .navigation_handlers import router as navigation_router

__all__ = [
    "start_router",
    "navigation_router"
]
