from aiogram import Dispatcher
from .main_menu import router as main_menu_router

def register_handlers(dp: Dispatcher) -> None:
    dp.include_router(main_menu_router)
