from aiogram.fsm.state import State, StatesGroup

class MenuStates(StatesGroup):
    INTRO_PAGE_1 = State()
    INTRO_PAGE_2 = State()
    INTRO_PAGE_3 = State()
    MAIN_MENU = State()
    NAVIGATION_MENU = State()
    PROFILE_MENU = State()
    HEROES_MENU = State()
    HERO_CLASS_MENU = State()
    BUILDS_MENU = State()
    VOTING_MENU = State()
    FEEDBACK_MENU = State()
    SETTINGS_MENU = State()
    STATISTICS_MENU = State()
    ACHIEVEMENTS_MENU = State()
    SEARCH_HERO = State()
    SEARCH_TOPIC = State()
    REPORT_BUG = State()
    RECEIVE_FEEDBACK = State()
    CHANGE_USERNAME = State()
    COMPARISON_STEP_1 = State()
    COMPARISON_STEP_2 = State()

class MainMenuState(StatesGroup):
    main = State()
    navigation = State()
    profile = State()

class NavigationState(StatesGroup):
    main = State()
    heroes = State()
    guides = State()

class ProfileState(StatesGroup):
    main = State()
    stats = State()
    achievements = State()
