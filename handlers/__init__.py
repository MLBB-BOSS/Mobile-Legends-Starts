from .start_handler import router as start_router

def setup_handlers(dispatcher):
    dispatcher.include_router(start_router)
