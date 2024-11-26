# /handlers/__init__.py
from .main_menu import router as main_menu_router
from .navigation import router as navigation_router
from .heroes import router as heroes_router
from .guides import router as guides_router

# Імпортуємо всі хендлери
routers = [
    main_menu_router,
    navigation_router,
    heroes_router,
    guides_router,
]

def setup_handlers(dispatcher):
    """Реєструємо всі хендлери"""
    for router in routers:
        dispatcher.include_router(router)
