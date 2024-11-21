# File: handlers/__init__.py

import logging
from aiogram import Router

logger = logging.getLogger(__name__)
logger.debug("Початок обробки імпортів у handlers/__init__.py")

try:
    from .start_command import router as start_router
    from .menu_handlers import router as menu_router
    from .hero_handlers import router as hero_router
    # Import other routers

    # Create main router
    main_router = Router()
    
    # Include all routers
    main_router.include_router(start_router)
    main_router.include_router(menu_router)
    main_router.include_router(hero_router)
    # Include other routers

    __all__ = ['main_router']

except Exception as e:
    logger.error(f"Помилка імпорту роутерів у handlers/__init__.py: {e}")
    raise
