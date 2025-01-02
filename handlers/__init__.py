# handlers/__init__.py

from aiogram import Dispatcher

def setup_handlers(dp: Dispatcher):
    from .start import register_start_handler
    from .navigation import register_navigation_handlers

    register_start_handler(dp)
    register_navigation_handlers(dp)
    # Додайте інші хендлери за необхідністю
