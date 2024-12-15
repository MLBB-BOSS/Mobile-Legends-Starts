#states/profile_states.py
from aiogram.dispatcher.filters.state import StatesGroup, State

class ProfileStates(StatesGroup):
    waiting_for_game_id = State()
