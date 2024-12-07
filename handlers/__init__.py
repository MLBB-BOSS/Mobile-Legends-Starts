# handlers/__init__.py

from .visual_handler import router as visual_router
# Імпортуйте інші роутери тут

def setup_handlers(dispatcher):
    dispatcher.include_router(visual_router)
    # Додайте інші роутери тут
