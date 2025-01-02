#states/state_groups.py
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

class BaseMenuState(StatesGroup):
    """Базовий клас для всіх меню"""
    main = State()

class MainMenuState(BaseMenuState):
    """Стани головного меню"""
    pass

class NavigationState(BaseMenuState):
    """Стани навігаційного меню"""
    heroes = State()
    builds = State()
    guides = State()
    tournaments = State()

class HeroesState(BaseMenuState):
    """Стани меню героїв"""
    list = State()
    info = State()
    meta = State()
    counter = State()

class ProfileState(BaseMenuState):
    """Стани меню профілю"""
    stats = State()
    settings = State()
    achievements = State()
