from aiogram import Dispatcher
from .main_menu import MainMenuHandler
from .intro_handler import IntroHandler

def setup_handlers(dp: Dispatcher) -> None:
    """Реєстрація всіх обробників"""
    # Створюємо екземпляр обробника інтро
    intro_handler = IntroHandler()
    dp.include_router(intro_handler.router)

    # Створюємо екземпляр обробника головного меню
    main_menu = MainMenuHandler()
    dp.include_router(main_menu.router)
