from .m6 import import router as register_m6_handlers
from .base import router as base_router

routers = [
    base_router,
]

def setup_handlers(dp):
    """Реєстрація всіх хендлерів"""
    for router in routers:
        dp.include_router(router)
