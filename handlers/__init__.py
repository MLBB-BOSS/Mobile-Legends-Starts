from typing import Optional
from aiogram import Dispatcher
from utils.message_utils import MessageManager
from handlers.intro_handler import router as intro_router
from handlers.menu_handler import router as menu_router
import logging
import os

logger = logging.getLogger(__name__)

# Логування для діагностики
logger.info(f"Current directory: {os.getcwd()}")
logger.info(f"Handlers path exists: {os.path.exists('handlers')}")
logger.info(f"Intro handler exists: {os.path.exists('handlers/intro_handler.py')}")
logger.info(f"Menu handler exists: {os.path.exists('handlers/menu_handler.py')}")

def setup_handlers(dp: Dispatcher, message_manager: Optional[MessageManager] = None):
    """
    Реєструє всі обробники в Dispatcher.
    """
    try:
        dp.include_router(intro_router)
        dp.include_router(menu_router)
        logger.info("Handlers successfully registered.")
    except Exception as e:
        logger.error(f"Error while registering handlers: {e}")
        raise
