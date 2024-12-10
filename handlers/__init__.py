# handlers/__init__.py

from .base import router as base_router
from .ai_handler import router as ai_router

def setup_handlers(dp):
    dp.include_router(base_router)
    dp.include_router(ai_router)
