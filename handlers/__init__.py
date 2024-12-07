# handlers/__init__.py

from .visual_handler import router as visual_router
# Імпортуйте інші роутери тут, наприклад:
# from .openai_handler import router as openai_router

def setup_handlers(dispatcher):
    dispatcher.include_router(visual_router)
    # Додайте інші роутери тут, наприклад:
    # dispatcher.include_router(openai_router)
