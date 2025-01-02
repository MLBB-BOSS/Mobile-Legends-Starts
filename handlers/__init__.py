# handlers/__init__.py

from aiogram import Dispatcher

def setup_handlers(dp: Dispatcher):
    from .start import register_start_handler
    from .navigation import router as navigation_router

    register_start_handler(dp)
    dp.include_router(navigation_router)
    # Додайте інші Routers за необхідністю
