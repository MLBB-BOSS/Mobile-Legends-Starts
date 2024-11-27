from .navigation import router as navigation_router
from .heroes import router as heroes_router
from .guides import router as guides_router
from .counter_picks import router as counter_picks_router
from .hero_classes import router as hero_classes_router
from .back import router as back_router

routers = [
    navigation_router,
    heroes_router,
    guides_router,
    counter_picks_router,
    hero_classes_router,
    back_router,
]

def setup_handlers(dp):
    """Реєстрація всіх хендлерів"""
    for router in routers:
        dp.include_router(router)
