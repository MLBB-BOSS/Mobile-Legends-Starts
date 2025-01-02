# handlers/__init__.py
from aiogram import Dispatcher
from .base import router as base_router
# If you have a features module, uncomment the next line:
# from .features import router as features_router

def setup_handlers(dp: Dispatcher):
    """
    Register all routers with the dispatcher.
    """
    # Include the base router
    dp.include_router(base_router)
    
    # If you have a features router, uncomment the next line:
    # dp.include_router(features_router)
