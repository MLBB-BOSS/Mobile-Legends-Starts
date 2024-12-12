from .base import router as base_router
from .tournaments import register_handlers as register_tournaments_handlers
from .meta import register_handlers as register_meta_handlers
from .m6 import register_handlers as register_m6_handlers

routers = [
    base_router,
]

def setup_handlers(dp):
    """Реєстрація всіх хендлерів"""
    for router in routers:
        dp.include_router(router)
