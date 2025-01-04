from aiogram.fsm.state import State, StatesGroup

class MainMenuState(StatesGroup):
    main = State()
    navigation = State()
    profile = State()

class NavigationState(StatesGroup):
    main = State()
    heroes = State()
    guides = State()

class ProfileState(StatesGroup):
    main = State()
    stats = State()
    achievements = State()
