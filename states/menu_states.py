from aiogram.fsm.state import State, StatesGroup

class IntroState(StatesGroup):
    """Intro states"""
    page_1 = State()
    page_2 = State()
    page_3 = State()

class MainMenuState(StatesGroup):
    """Main menu states"""
    main = State()
    navigation = State()
    profile = State()

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

class NavigationState(StatesGroup):
    """Navigation menu states"""
    main = State()
    select_hero = State()
    hero_details = State()

class ProfileState(StatesGroup):
    """Profile section states"""
    main = State()
    edit = State()
    view = State()
