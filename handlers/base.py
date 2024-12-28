# handlers/base.py

import logging
from . import setup_handlers

logger = logging.getLogger(__name__)

def setup_handlers(dp):
    """
    Підключаємо мінімальні хендлери для старту + головне меню
    """
    from .start_intro import router as start_intro_router
    from .main_menu import router as main_menu_router

    dp.include_router(start_intro_router)
    dp.include_router(main_menu_router)

    logger.info("Handlers for start + main menu successfully set up.")
