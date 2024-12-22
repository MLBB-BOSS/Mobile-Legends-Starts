from aiogram.fsm.state import StatesGroup, State

class MenuStates(StatesGroup):
    # Головне меню та підменю
    INTRO_PAGE_1 = State()
    INTRO_PAGE_2 = State()
    INTRO_PAGE_3 = State()
    MAIN_MENU = State()
    NAVIGATION_MENU = State()
    PROFILE_MENU = State()
    SETTINGS_MENU = State()
    SETTINGS_SUBMENU = State()
    HELP_MENU = State()
    HELP_SUBMENU = State()

    # Меню персонажів
    HEROES_MENU = State()
    HERO_CLASS_MENU = State()
    SEARCH_HERO = State()
    CHALLENGES_MENU = State()
    COMPARISON_STEP_1 = State()

    # Гайди, контр-піки та білди
    GUIDES_MENU = State()
    COUNTER_PICKS_MENU = State()
    BUILDS_MENU = State()
    VOTING_MENU = State()

    # Меню статистики
    STATISTICS_MENU = State()
    ACHIEVEMENTS_MENU = State()

    # Турніри та команди
    TOURNAMENTS_MENU = State()
    TEAMS_MENU = State()
    MY_TEAM_MENU = State()

    # Meta, M6, GPT
    META_MENU = State()
    M6_MENU = State()
    GPT_MENU = State()

    # Торгівля, бафи та додаткові функції
    TRADING_MENU = State()
    BUST_MENU = State()

    # Інтерактивні стани
    SEARCH_TOPIC = State()
    CHANGE_USERNAME = State()
    RECEIVE_FEEDBACK = State()
    REPORT_BUG = State()
    SELECT_LANGUAGE = State()

async def increment_step(state):
    data = await state.get_data()
    step_count = data.get("step_count", 0) + 1
    if step_count >= 3:
        await state.clear()
        step_count = 0
    await state.update_data(step_count=step_count)
