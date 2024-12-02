from .base import router as base_router
from .callbacks import callbacks_router
from .heroes import heroes_router
from .main_menu import menu_router
from .start_handler import start_router

# Список усіх роутерів
routers = [
    start_router,
    menu_router,
    heroes_router,
    callbacks_router,
    base_router,
]

def setup_handlers(dp):
    """
    Реєстрація всіх хендлерів у диспетчері.
    """
    for router in routers:
        dp.include_router(router)
