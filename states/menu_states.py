from aiogram.fsm.state import State, StatesGroup

class MenuStates(StatesGroup):
    # Приклад станів
    CHOOSING_OPTION = State()
    WAITING_FOR_INPUT = State()
