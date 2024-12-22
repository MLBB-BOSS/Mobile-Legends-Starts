# utils/state_utils.py

from aiogram.fsm.context import FSMContext

async def increment_step(state: FSMContext):
    data = await state.get_data()
    step_count = data.get("step_count", 0) + 1
    if step_count >= 3:
        await state.clear()
        step_count = 0
    await state.update_data(step_count=step_count)
