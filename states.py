from aiogram.fsm.state import State, StatesGroup

class MenuStates(StatesGroup):
    # Existing states
    MAIN_MENU = State()
    CHALLENGES_MENU = State()
    GUIDES_MENU = State()
    BUST_MENU = State()
    TEAMS_MENU = State()
    TRADING_MENU = State()
    SETTINGS_MENU = State()
    SETTINGS_SUBMENU = State()
    SELECT_LANGUAGE = State()
    PROFILE_MENU = State()
    STATS_MENU = State()
    ACHIEVEMENTS_MENU = State()
    FEEDBACK_MENU = State()
    HELP_MENU = State()
    MY_TEAM_MENU = State()
    GPT_MENU = State()
    HELP_SUBMENU = State()
    CHANGE_USERNAME = State()
    RECEIVE_FEEDBACK = State()
    REPORT_BUG = State()
    
    # Previously suggested states
    TOURNAMENTS_MENU = State()
    HEROES_MENU = State()
    COUNTER_PICKS_MENU = State()
    BUILDS_MENU = State()
    VOTING_MENU = State()
    NAVIGATION_MENU = State()
    
    # New state causing the current error
    META_MENU = State()  # Add this state for the meta game menu
