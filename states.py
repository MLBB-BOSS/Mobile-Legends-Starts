# states.py

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import logging

logger = logging.getLogger(__name__)

class MenuStates(StatesGroup):
    INTRO_PAGE_1 = State()
    INTRO_PAGE_2 = State()
    INTRO_PAGE_3 = State()
    MAIN_MENU = State()
    NAVIGATION_MENU = State()
    HEROES_MENU = State()
    HERO_CLASS_MENU = State()
    GUIDES_MENU = State()
    COUNTER_PICKS_MENU = State()
    BUILDS_MENU = State()
    VOTING_MENU = State()
    PROFILE_MENU = State()
    STATISTICS_MENU = State()
    ACHIEVEMENTS_MENU = State()
    SETTINGS_MENU = State()
    CHANGE_USERNAME = State()
    RECEIVE_FEEDBACK = State()
    REPORT_BUG = State()
    HELP_MENU = State()
    SEARCH_HERO = State()
    SEARCH_TOPIC = State()
    GPT_MENU = State()
    M6_MENU = State()
    META_MENU = State()

async def increment_step(state: FSMContext, max_steps: int = 3):
    """
    Increments the step in the state data. Resets to MAIN_MENU after max_steps.
    """
    data = await state.get_data()
    step = data.get("step", 0) + 1
    logger.info(f"Current step: {step}")
    if step >= max_steps:
        # Save necessary data before clearing
        interactive_message_id = data.get("interactive_message_id")
        bot_message_id = data.get("bot_message_id")
        await state.clear()
        await state.set_state(MenuStates.MAIN_MENU)
        await state.update_data(interactive_message_id=interactive_message_id, bot_message_id=bot_message_id)
        logger.info("State reset to MAIN_MENU")
    else:
        await state.update_data(step=step)
        logger.info(f"Step incremented to {step}")