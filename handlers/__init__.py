# File: handlers/__init__.py

import logging
from aiogram import Router

logger = logging.getLogger(__name__)
logger.debug("Початок обробки імпортів у handlers/__init__.py")

try:
    from .start_command import router as start_router
    from .menu_handlers import router as menu_router
    from .profile_handlers import router as profile_router
    from .navigation_handlers import router as navigation_router

    # Create main router and include all other routers
    main_router = Router()
    main_router.include_router(start_router)
    main_router.include_router(menu_router)
    main_router.include_router(profile_router)
    main_router.include_router(navigation_router)

    __all__ = [
        'main_router',
        'start_router',
        'menu_router',
        'profile_router',
        'navigation_router'
    ]

except Exception as e:
    logger.error(f"Помилка імпорту роутерів у handlers/__init__.py: {e}")
    raise
