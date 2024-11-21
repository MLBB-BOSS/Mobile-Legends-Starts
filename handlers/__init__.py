# File: handlers/__init__.py

from .start_command import router as start_router
from .hero_commands import router as hero_router
from .message_handlers import router as message_router
from .menu_handlers import router as menu_router
from .error_handler import router as error_router

__all__ = ['start_router', 'hero_router', 'message_router', 'menu_router', 'error_router']
