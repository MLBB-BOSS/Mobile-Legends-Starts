from enum import auto
from aiogram.fsm.state import State, StatesGroup

class IntroState(StatesGroup):
    """Intro section states"""
    page_1 = State()
    page_2 = State()
    page_3 = State()

class MainMenuState(StatesGroup):
    """Main menu states"""
    main = State()
    navigation = State()
    profile = State()
