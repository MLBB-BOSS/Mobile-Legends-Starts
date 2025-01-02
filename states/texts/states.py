# states/states.py

from aiogram.fsm.state import State, StatesGroup

class MenuStates(StatesGroup):
    MAIN_MENU = State()
    NAVIGATION_MENU = State()
    HEROES_MENU = State()
    MAP_MENU = State()
    ITEMS_MENU = State()
    RANKS_MENU = State()
    GUIDES_MENU = State()
    META_MENU = State()
