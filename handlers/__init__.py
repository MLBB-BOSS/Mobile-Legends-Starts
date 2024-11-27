from .navigation import router as navigation_router
from .heroes import router as heroes_router
from .back import router as back_router

routers = [
    navigation_router,
    heroes_router,
    back_router,
]

def setup_handlers(dp):
    """Реєстрація всіх хендлерів"""
    for router in routers:
        dp.include_router(router)
