# File: handlers/__init__.py

import logging
from aiogram import Router, F
from typing import List, Optional

logger = logging.getLogger(__name__)

def create_main_router() -> Optional[Router]:
    """
    Creates and configures the main router with all sub-routers.
    Returns None if initialization fails.
    """
    try:
        logger.debug("Starting router initialization")
        
        # Create main router
        main_router = Router(name="main_router")
        
        # Import routers with explicit error handling
        from .start_command import router as start_router
        from .menu_handlers import router as menu_router
        from .hero_handlers import router as hero_router
        from .profile_handlers import router as profile_router
        from .navigation_handlers import router as navigation_router

        # Define router configuration with priorities
        routers_config: List[tuple[Router, dict]] = [
            (start_router, {"name": "start_commands", "filter": F.text.startswith("/")}),
            (menu_router, {"name": "menu_handlers"}),
            (hero_router, {"name": "hero_handlers"}),
            (profile_router, {"name": "profile_handlers"}),
            (navigation_router, {"name": "navigation_handlers"})
        ]

        # Include routers with their configurations
        for router, config in routers_config:
            try:
                main_router.include_router(router, **config)
                logger.debug(f"Successfully included router: {config['name']}")
            except Exception as router_error:
                logger.error(f"Failed to include router {config['name']}: {router_error}")
                continue

        logger.info("All routers successfully initialized")
        return main_router

    except ImportError as import_error:
        logger.error(f"Failed to import router module: {import_error}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during router initialization: {e}")
        raise

try:
    # Initialize main router
    main_router = create_main_router()
    if main_router is None:
        raise RuntimeError("Failed to initialize main router")

    __all__ = ['main_router']

except Exception as e:
    logger.critical(f"Critical error in handlers initialization: {e}")
    raise
