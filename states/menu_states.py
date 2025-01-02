# states/menu_states.py

from aiogram.fsm.state import State, StatesGroup

class MenuStates(StatesGroup):
    """Стани меню бота"""
    # Базові стани
    START = State()
    MAIN_MENU = State()
    
    # Стани навігації
    NAVIGATION_MENU = State()
    HEROES_MENU = State()
    MAP_MENU = State()
    ITEMS_MENU = State()
    RANKS_MENU = State()
    GUIDES_MENU = State()
    META_MENU = State()
    
    # Стани профілю
    PROFILE_MENU = State()
    PROFILE_EDIT = State()
