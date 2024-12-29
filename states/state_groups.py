#states/state_groups.py
from aiogram.fsm.state import State, StatesGroup

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
