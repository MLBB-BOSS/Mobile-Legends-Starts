# utils/state_utils.py

from aiogram.fsm.context import FSMContext
from states import MenuStates
import logging

logger = logging.getLogger(__name__)

async def transition_state(state: FSMContext, new_state: MenuStates):
    await state.clear()
    await state.set_state(new_state)
    logger.info(f"Transitioned to state: {new_state.name}")
