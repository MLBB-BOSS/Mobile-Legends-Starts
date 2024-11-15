from aiogram.fsm.state import State, StatesGroup

class RegistrationStates(StatesGroup):
    waiting_for_nickname = State()
    waiting_for_email = State()
    waiting_for_game_id = State()
