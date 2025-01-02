# states/navigation_state.py

from aiogram.fsm.state import StatesGroup, State

class NavigationState(StatesGroup):
    heroes = State()
    # Додайте інші стани за потребою
