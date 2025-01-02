from aiogram.fsm.state import State, StatesGroup

class MainMenuState(StatesGroup):
    main = State()
    settings = State()
    profile = State()
    tournaments = State()
    screenshots = State()

class ProfileState(StatesGroup):
    stats = State()
    settings = State()
    achievements = State()

__all__ = ['MainMenuState', 'ProfileState']
