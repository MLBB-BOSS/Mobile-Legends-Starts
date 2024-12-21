# Приклад простої реалізації transition_state
from states import MenuStates

async def transition_state(state: FSMContext, new_state: MenuStates):
    """
    Очищає попередні дані стану та переходить до нового стану.
    """
    await state.clear()
    await state.set_state(new_state)
