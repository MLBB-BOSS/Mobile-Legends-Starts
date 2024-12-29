from aiogram import Dispatcher
from .main_menu import MainMenuHandler

def setup_handlers(dp: Dispatcher) -> None:
    """Реєстрація всіх обробників"""
    # Створюємо екземпляр обробника головного меню
    main_menu = MainMenuHandler()
    
    # Реєструємо роутер головного меню
    dp.include_router(main_menu.router)
