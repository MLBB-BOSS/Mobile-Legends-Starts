from handlers.start_handler import router as start_router
from handlers.base import router as base_routerfrom .start_handler import router as start_router

def setup_handlers(dispatcher):
    dispatcher.include_router(start_router)
    dispatcher.include_router(base_router)
