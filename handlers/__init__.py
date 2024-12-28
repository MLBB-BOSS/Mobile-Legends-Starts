# handlers/__init__.py
from aiogram import Dispatcher

# Підключаємо хендлери інтро (якщо є)
from .start_intro import router as start_intro_router

# Підключаємо хендлер головного меню
from .main_menu import router as main_menu_router

# Підключаємо навігацію
from .navigation import router as navigation_router

# Підключаємо профіль
from .profile import router as profile_router

def setup_handlers(dp: Dispatcher):
    # Підключаємо інтро (якщо треба)
    dp.include_router(start_intro_router)

    # Головне меню
    dp.include_router(main_menu_router)

    # Навігація
    dp.include_router(navigation_router)

    # Профіль
    dp.include_router(profile_router)
