# handlers/__init__.py

from .base import router as base_router
from .progress import router as progress_router
from .missing_handlers import router as missing_handlers_router
# Додайте інші маршрутизатори тут

routers = [
    base_router,
    progress_router,
    missing_handlers_router,
    # Додайте інші маршрутизатори сюди
]

def setup_handlers(dp):
    for router in routers:
        dp.include_router(router)