# states/menu_states.py
from aiogram.fsm.state import State, StatesGroup

class IntroState(StatesGroup):
    page_1 = State()
    page_2 = State()
    page_3 = State()

class MainMenuState(StatesGroup):
    main = State()
    profile = State()
    stats = State()
    team = State()
    tournament = State()
