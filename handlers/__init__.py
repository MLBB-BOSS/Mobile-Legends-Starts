from .base import router as base_router
from .profile import profile_router  # Додано імпорт profile_router

def setup_handlers(dp):
    """Реєстрація всіх хендлерів"""
    dp.include_router(base_router)  # Реєстрація base_router
    dp.include_router(profile_router)  # Реєстрація profile_router
