# handlers/__init__.py
from aiogram import Dispatcher
from typing import Optional
from logging import getLogger
from utils.message_utils import MessageManager
from .intro_handler import router as intro_router
from .menu_handler import MenuHandler
from texts import WELCOME_NEW_USER_TEXT, INTRO_PAGE_1_TEXT, INTRO_PAGE_2_TEXT, INTRO_PAGE_3_TEXT

logger = getLogger(__name__)

def setup_handlers(dp: Dispatcher, message_manager: Optional[MessageManager] = None) -> None:
    """Setup all handlers"""
    try:
        handlers = [
            IntroHandler(message_manager),
            MenuHandler(message_manager)
        ]
        
        for handler in handlers:
            dp.include_router(handler.router)
            logger.info(f"Registered {handler.__class__.__name__}")
            
    except Exception as e:
        logger.error(f"Error setting up handlers: {e}")
        raise

    def setup_handlers(dp: Dispatcher):
    """
    Реєструє всі обробники в Dispatcher.
    """
    dp.include_router(intro_router)
