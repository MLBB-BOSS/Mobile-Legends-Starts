# handlers/__init__.py

from aiogram import Dispatcher
from .start import router as start_router
from .navigation import router as navigation_router

def setup_handlers(dp: Dispatcher):
    # Include routers
    dp.include_router(start_router)
    dp.include_router(navigation_router)
