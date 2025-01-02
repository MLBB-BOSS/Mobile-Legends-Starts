from aiogram.fsm.state import State, StatesGroup

class MainMenuState(StatesGroup):
    """Станів для головного меню"""
    main = State()
    settings = State()
    profile = State()
    tournaments = State()
    screenshots = State()

class IntroState(StatesGroup):
    """Станів для вступного меню"""
    INTRO_PAGE_1 = State()
    INTRO_PAGE_2 = State()
    INTRO_PAGE_3 = State()

__all__ = ['MainMenuState', 'IntroState']
