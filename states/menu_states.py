from aiogram.fsm.state import State, StatesGroup

class MainMenuState(StatesGroup):
    main = State()

class NavigationState(StatesGroup):
    main = State()

class ProfileState(StatesGroup):
    main = State()