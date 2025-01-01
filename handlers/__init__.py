# handlers/__init__.py
from aiogram import Dispatcher
from .intro_handler import IntroHandler
from .main_menu import MainMenuHandler
import logging

logger = logging.getLogger(__name__)

def setup_handlers(dp: Dispatcher) -> None:
    """Setup all handlers"""
    try:
        handlers = [
            IntroHandler(),
            MainMenuHandler()
        ]
        
        for handler in handlers:
            dp.include_router(handler.router)
            logger.info(f"Registered {handler.__class__.__name__}")
            
    except Exception as e:
        logger.error(f"Error setting up handlers: {e}")
        raise
