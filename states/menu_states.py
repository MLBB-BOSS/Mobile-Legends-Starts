# states/menu_states.py

from aiogram.fsm.state import State, StatesGroup

class IntroState(StatesGroup):
    """Стани для вступної частини бота"""
    page_1 = State()
    page_2 = State()
    page_3 = State()

class MainMenuState(StatesGroup):
    """Стани для головного меню"""
    main = State()
    navigation = State()
    profile = State()

class ProfileState(StatesGroup):
    """Стани для розділу профілю"""
    main = State()
    settings = State()
    statistics = State()
    achievements = State()

class NavigationState(StatesGroup):
    """Стани для навігаційного меню"""
    main = State()
    heroes = State()
    builds = State()
    guides = State()
    tournaments = State()
    teams = State()

class HeroState(StatesGroup):
    """Стани для розділу героїв"""
    class_selection = State()
    hero_selection = State()
    hero_info = State()

class TournamentState(StatesGroup):
    """Стани для розділу турнірів"""
    main = State()
    creation = State()
    viewing = State()
    registration = State()
