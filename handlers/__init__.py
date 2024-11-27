from .start import router as start_router
from .main_menu import router as main_menu_router
from .navigation import router as navigation_router
from .heroes import router as heroes_router
from .back import router as back_router  # Додаємо новий хендлер

routers = [
    start_router,
    main_menu_router,
    navigation_router,
    heroes_router,
    back_router  # Реєструємо хендлер "Назад"
]

def setup_handlers(dp):
    """Підключаємо всі хендлери"""
    for router in routers:
        dp.include_router(router)
