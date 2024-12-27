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

    # New states to add based on the handlers
    TOURNAMENTS_MENU = State()      # Used in handlers causing the current error
    HEROES_MENU = State()           # Used in base.py
    COUNTER_PICKS_MENU = State()    # Used in base.py
    BUILDS_MENU = State()           # Used in base.py
    VOTING_MENU = State()           # Used in base.py
    NAVIGATION_MENU = State()       # Used in navigation handlers
