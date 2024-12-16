from .base import router as base_router
from .profile import profile_router  # Додано імпорт profile_router

routers = [
    base_router,
    profile_router,  # Додаємо profile_router до списку
]

def setup_handlers(dp):
    """Реєстрація всіх хендлерів"""
    for router in routers:
        dp.include_router(router)
