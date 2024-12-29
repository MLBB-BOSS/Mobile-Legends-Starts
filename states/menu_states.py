# states/menu_states.py
from aiogram.fsm.state import State, StatesGroup

class MenuStates(StatesGroup):
    MAIN_MENU = State()
    NAVIGATION_MENU = State()
    HEROES_MENU = State()
    PROFILE_MENU = State()
    SETTINGS_MENU = State()
    STATISTICS_MENU = State()
    ACHIEVEMENTS_MENU = State()
    FEEDBACK_MENU = State()
    HELP_MENU = State()
    GUIDES_MENU = State()
    TOURNAMENTS_MENU = State()
    TEAMS_MENU = State()
    TRADING_MENU = State()
    CHALLENGES_MENU = State()
    BUST_MENU = State()
    GPT_MENU = State()
    M6_MENU = State()
    META_MENU = State()
    BUILDS_MENU = State()
    VOTING_MENU = State()
    COUNTER_PICKS_MENU = State()
    INTRO_PAGE_1 = State()            # 96. Перша сторінка вступу
    INTRO_PAGE_2 = State()            # 97. Друга сторінка вступу
    INTRO_PAGE_3 = State()            # 98. Третя сторінка вступу
    INTRO_COMPLETE = State()          # 99. 
