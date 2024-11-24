from aiogram import Dispatcher

from .main_menu import register_handlers_main_menu
from .navigation import register_handlers_navigation

def register_handlers(dp: Dispatcher):
    register_handlers_main_menu(dp)
    register_handlers_navigation(dp)
