# File: handlers/__init__.py

import logging

logger = logging.getLogger(__name__)
logger.debug("Початок обробки імпортів у handlers/__init__.py")

try:
    from .start_command import router as start_router
    from .menu_handlers import router as menu_router
    
    __all__ = ['start_router', 'menu_router']
    
except ImportError as e:
    logger.error(f"Помилка імпорту роутерів у handlers/__init__.py: {e}")
    raise
