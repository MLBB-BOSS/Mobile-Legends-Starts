# handlers/__init__.py

from aiogram import Dispatcher

def setup_handlers(dp: Dispatcher):
    from .start import router as start_router
    from .navigation import router as navigation_router

    # Include both routers
    dp.include_router(start_router)
    dp.include_router(navigation_router)
    # Додайте інші Routers за необхідністю
