from .start_handler import router as start_router
from .base import router as base_router

def setup_handlers(dispatcher):
    dispatcher.include_router(start_router)
    dispatcher.include_router(base_router)
