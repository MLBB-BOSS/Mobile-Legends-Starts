# handlers/__init__.py
from aiogram import Dispatcher
from typing import Optional
from logging import getLogger
from utils.message_utils import MessageManager
from .intro_handler import IntroHandler
from .menu_handler import MenuHandler

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
