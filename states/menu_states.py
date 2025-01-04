from aiogram.fsm.state import State, StatesGroup

class MainMenuState(StatesGroup):
    main = State(Головне меню)

class NavigationState(StatesGroup):
    main = State(Навігація)

class ProfileState(StatesGroup):
    main = State(Профіль)
