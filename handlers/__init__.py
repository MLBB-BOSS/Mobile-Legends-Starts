# /handlers/__init__.py
from .start import router as start_router
from .main_menu import router as main_menu_router
from .navigation import router as navigation_router
from .heroes import router as heroes_router
from .guides import router as guides_router
from .help import router as help_router

routers = [
    start_router,
    main_menu_router,
    navigation_router,
    heroes_router,
    guides_router,
    help_router
]

def setup_handlers(dp):
    """Функція для підключення всіх хендлерів до диспетчера"""
    for router in routers:
        dp.include_router(router)
