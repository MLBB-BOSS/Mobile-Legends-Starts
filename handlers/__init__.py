# handlers/__init__.py

from .start_handler import router as start_router
# Імпортуйте інші роутери тут, наприклад:
# from .visual_handler import router as visual_router

def setup_handlers(dispatcher):
    dispatcher.include_router(start_router)
    # dispatcher.include_router(visual_router)
    # Додайте інші роутери тут
