# handlers/__init__.py

from aiogram import Dispatcher
from .start_intro import router as start_intro_router
from .main_menu import router as main_menu_router

# Не підключаємо все інше. Коли доробимо – тоді додаємо.
# from .navigation.menu import router as navigation_router
# from .profile.menu import router as profile_router
# ...

def setup_handlers(dp: Dispatcher):
    dp.include_router(start_intro_router)
    dp.include_router(main_menu_router)
