from aiogram import Dispatcher
from .intro_handler import IntroHandler
from .main_menu import MainMenuHandler
import logging

logger = logging.getLogger(__name__)

def setup_handlers(dp: Dispatcher) -> None:
    """Реєстрація всіх обробників"""
    try:
        # Створюємо екземпляр обробника інтро
        intro_handler = IntroHandler()
        dp.include_router(intro_handler.router)
        logger.info("Intro handler registered successfully")

        # Створюємо екземпляр обробника головного меню
        main_menu = MainMenuHandler()
        dp.include_router(main_menu.router)
        logger.info("Main menu handler registered successfully")
        
    except Exception as e:
        logger.error(f"Error setting up handlers: {e}")
        raise
