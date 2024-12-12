from .base import router as base_router
from .m6 import router as m6_router
from .meta import router as meta_router
from .tournaments import router as tournaments_router

routers = [
    base_router,
    m6_router,
    meta_router,
    tournaments_router,
]

def setup_handlers(dp):
    """Реєстрація всіх хендлерів"""
    for router in routers:
        dp.include_router(router)
