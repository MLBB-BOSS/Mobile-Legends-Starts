# states/menu_states.py
from aiogram.fsm.state import State, StatesGroup

class MenuStates(StatesGroup):
    # Стани для інтро-сторінок
    INTRO_PAGE_1 = State()
    INTRO_PAGE_2 = State()
    INTRO_PAGE_3 = State()
    
    # Основні стани меню
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

    # Стани для підменю героїв
    HERO_CLASS_SELECTION = State()
    HERO_LIST = State()
    HERO_DETAILS = State()
    
    # Стани для налаштувань
    LANGUAGE_SELECTION = State()
    NOTIFICATION_SETTINGS = State()
    
    # Стани для турнірів
    TOURNAMENT_CREATION = State()
    TOURNAMENT_LIST = State()
    TOURNAMENT_DETAILS = State()
    
    # Стани для команд
    TEAM_CREATION = State()
    TEAM_LIST = State()
    TEAM_DETAILS = State()
