from .start import router as start_router
from .main_menu import router as main_menu_router
from .navigation import router as navigation_router
from .heroes import router as heroes_router

routers = [
    start_router,
    main_menu_router,
    navigation_router,
    heroes_router
]

def setup_handlers(dp):
    """Підключаємо всі хендлери до Dispatcher"""
    for router in routers:
        dp.include_router(router)
