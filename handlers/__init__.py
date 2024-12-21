# handlers/__init__.py

from .base import router as base_router
# Імпортуйте інші маршрутизатори з інших файлів, наприклад:
# from .progress import router as progress_router
# from .feedback import router as feedback_router

routers = [
    base_router,
    # progress_router,
    # feedback_router,
    # Додайте інші маршрутизатори тут
]

def setup_handlers(dp: Dispatcher):
    for router in routers:
        dp.include_router(router)