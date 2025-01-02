# handlers/__init__.py
from typing import Optional
from aiogram import Dispatcher
from utils.message_utils import MessageManager  # Add this import
from handlers.intro_handler import router as intro_router
from handlers.menu_handler import router as menu_router
from aiogram.exceptions import TelegramBadRequest
def setup_handlers(dp: Dispatcher, message_manager: Optional[MessageManager] = None):
    """
    Реєструє всі обробники в Dispatcher.
    """
    dp.include_router(intro_router)
    dp.include_router(menu_router)
    # Додайте додаткову логіку для message_manager, якщо потрібно
