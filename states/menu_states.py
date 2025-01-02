from aiogram.fsm.state import State, StatesGroup

class MenuStates(StatesGroup):
    """Станів для меню"""
    MAIN_MENU = State()
    PROFILE = State()
    STATS = State()
    TEAM = State()
    TOURNAMENT = State()

class IntroState(StatesGroup):
    """Станів для інтро"""
    INTRO_PAGE_1 = State()
    INTRO_PAGE_2 = State()
    INTRO_PAGE_3 = State()

class MenuStates(StatesGroup):
    """Станів для меню"""
    MAIN_MENU = State()
    INTRO_PAGE_1 = State()
    INTRO_PAGE_2 = State()
    INTRO_PAGE_3 = State()
    PROFILE = State()
    STATS = State()
    TEAM = State()
    TOURNAMENT = State()# states/menu_states.py
