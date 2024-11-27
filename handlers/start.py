from .start import router as start_router
from .main_menu import router as main_menu_router
from .navigation import router as navigation_router
from .heroes import router as heroes_router
from .guides import router as guides_router

routers = [
    start_router,
    main_menu_router,
    navigation_router,
    heroes_router,
    guides_router
]

def setup_handlers(dp):
    """Реєстрація всіх хендлерів"""
    for router in routers:
        dp.include_router(router)
