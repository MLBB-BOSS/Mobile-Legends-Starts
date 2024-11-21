# handlers/__init__.py

import logging

logger = logging.getLogger(__name__)
logger.debug("Початок обробки імпортів у handlers/__init__.py")

try:
    from .start_command import router as start_router
    from .menu_handlers import router as menu_router
    from .message_handlers import router as message_router
    logger.debug("Імпорти роутерів успішно виконано у handlers/__init__.py")
except ImportError as e:
    logger.exception(f"Помилка імпорту роутерів у handlers/__init__.py: {e}")
    raise
