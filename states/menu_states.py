# states/menu_states.py
from aiogram.fsm.state import State, StatesGroup

class IntroState(StatesGroup):
    """Стани інтро-повідомлень"""
    page_1 = State()
    page_2 = State()
    page_3 = State()

class BaseState(StatesGroup):
    """Базовий клас для всіх станів"""
    main = State()

class MainMenuState(BaseState):
    """Стани головного меню"""
    pass

class NavigationState(BaseState):
    """Стани навігації"""
    heroes = State()
    builds = State()
    guides = State()
    tournaments = State()
    teams = State()
    challenges = State()
    bust = State()
    trading = State()

class ProfileState(BaseState):
    """Стани профілю"""
    stats = State()
    team = State()
    achievements = State()
    settings = State()
    feedback = State()
    help = State()
    gpt = State()
