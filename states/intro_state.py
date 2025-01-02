# states/intro_state.py

from aiogram.fsm.state import StatesGroup, State

class IntroState(StatesGroup):
    page_1 = State()
    page_2 = State()
    page_3 = State()
