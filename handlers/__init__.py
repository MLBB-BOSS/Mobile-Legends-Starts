from aiogram import Dispatcher
from .intro_handler import router as intro_router
from .menu_handler import router as menu_router  # Додайте інші обробники, якщо необхідно
from keyboards.inline_menus import get_main_menu_keyboard

def setup_handlers(dp: Dispatcher):
    """
    Реєструє всі обробники в Dispatcher.
    """
    dp.include_router(intro_router)
    dp.include_router(menu_router)
