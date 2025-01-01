# states/base.py

from aiogram.fsm.state import State, StatesGroup

class BaseState(StatesGroup):
    """Базовий клас для станів"""
    
    @classmethod
    def get_state_name(cls, state: State) -> str:
        """Отримати назву стану"""
        return state.state

    @classmethod
    def get_all_states(cls) -> list:
        """Отримати всі стани групи"""
        return [state for state in cls.all_states]
