# states/profile_state.py

from aiogram.fsm.state import StatesGroup, State

class ProfileState(StatesGroup):
    stats = State()
    achievements = State()
    settings = State()
    feedback = State()
    help = State()
    gpt = State()
    # Додайте інші стани за потребою
