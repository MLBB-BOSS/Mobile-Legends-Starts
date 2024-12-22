from aiogram.fsm.state import StatesGroup, State

class MenuStates(StatesGroup):
    MAIN_MENU = State()
    HEROES_MENU = State()
    # Інші стани...
    COMPARISON_STEP_1 = State()  # Додайте цей стан
