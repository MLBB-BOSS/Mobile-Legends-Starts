from .m6 import router as m6_router
from .base import router as base_router

routers = [
    base_router,
]

def setup_handlers(dp):
    """Реєстрація всіх хендлерів"""
    for router in routers:
        dp.include_router(router)
