# handlers/__init__.py

from aiogram import Dispatcher
from .start_intro import router as start_intro_router
from .main_menu import router as main_menu_router

# Якщо не готові модулі navigation та profile, не підключайте їх поки
# from .navigation.menu import router as navigation_router
# from .profile.menu import router as profile_router

def setup_handlers(dp: Dispatcher):
    """
    Підключаємо тільки ті хендлери, які точно працюють:
    /start, сторінки інтро та головне меню.
    """
    dp.include_router(start_intro_router)
    dp.include_router(main_menu_router)

    # Коли доробите інші файли:
    # dp.include_router(navigation_router)
    # dp.include_router(profile_router)
