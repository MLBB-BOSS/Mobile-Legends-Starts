# handlers/__init__.py

from .start_handler import router as start_router
from .base import router as base_router
from .visual_handler import router as visual_router
from .callbacks import router as callbacks_router
# Імпортуйте інші роутери тут, наприклад:
# from .openai_handler import router as openai_router

def setup_handlers(dispatcher):
    dispatcher.include_router(start_router)
    dispatcher.include_router(base_router)
    dispatcher.include_router(visual_router)
    dispatcher.include_router(callbacks_router)
    # Додайте інші роутери тут
    # dispatcher.include_router(openai_router)
