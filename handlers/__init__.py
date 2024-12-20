from .base import router as base_router
from .missing_handlers import router as missing_router  # Новий хендлер

routers = [
    base_router,
    missing_router,  # Додано новий маршрутизатор
]

def setup_handlers(dp):
    """Реєстрація всіх хендлерів"""
    for router in routers:
        dp.include_router(router)