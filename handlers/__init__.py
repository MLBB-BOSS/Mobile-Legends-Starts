# handlers/__init__.py
from .base import router as base_router

__all__ = ['base_router']  # Додайте інші обробники до цього списку

def setup_handlers(dp):
    dp.include_router(base_router)
    # Якщо у вас будуть інші роутери, додайте їх тут
    # Наприклад:
    # from .challenges import router as challenges_router
    # dp.include_router(challenges_router)
