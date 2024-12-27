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
    # New state causing the current error
    M6_MENU = State()  # Add this state for the M6 menu section
    # Additional states found in handlers
    HERO_LIST_MENU = State()      # Used in meta menu for hero list
    RECOMMENDATIONS_MENU = State() # Used in meta menu for recommendations
    UPDATES_MENU = State()        # Used in meta menu for updates
    BACK_TO_MAIN = State()
    # Hero comparison states
    COMPARISON_STEP_1 = State()  # Вибір першого героя/предмета для порівняння
    COMPARISON_STEP_2 = State()  # Вибір другого героя/предмета для порівняння
    COMPARISON_RESULT = State()  # Показ результатів порівняння
    # Hero search and management states
    SEARCH_HERO = State()           # Стан пошуку героя
    HERO_DETAILS = State()          # Перегляд деталей героя
    HERO_SELECTION = State()        # Вибір героя зі списку
    HERO_FILTER = State()           # Фільтрація героїв
    HERO_SORT = State()             # Сортування героїв
    HERO_FAVORITES = State()        # Обрані герої
    HERO_STATISTICS = State()       # Статистика героя
    # Search System States
    SEARCH_TOPIC = State()
SEARCH_CATEGORY = State()
SEARCH_RESULT = State()
SEARCH_FILTER = State()
SEARCH_HISTORY = State()
SEARCH_FAVORITES = State()

# Tournament System States
TOURNAMENT_CREATE = State()
TOURNAMENT_EDIT = State()
TOURNAMENT_JOIN = State()
TOURNAMENT_LIST = State()
TOURNAMENT_BRACKET = State()
TOURNAMENT_RESULTS = State()
TOURNAMENT_RULES = State()

# Team Management States
TEAM_CREATE = State()
TEAM_EDIT = State()
TEAM_INVITE = State()
TEAM_ROSTER = State()
TEAM_SETTINGS = State()
TEAM_STATS = State()

# Match States
MATCH_CREATE = State()
MATCH_JOIN = State()
MATCH_RESULT = State()
MATCH_HISTORY = State()
MATCH_REPORT = State()

# Content Management States
CONTENT_CREATE = State()
CONTENT_EDIT = State()
CONTENT_DELETE = State()
CONTENT_REVIEW = State()

# Achievement System States
ACHIEVEMENT_VIEW = State()
ACHIEVEMENT_PROGRESS = State()
ACHIEVEMENT_CLAIM = State()

# Community States
COMMUNITY_CHAT = State()
COMMUNITY_EVENTS = State()
COMMUNITY_RULES = State()

# Notification States
NOTIFICATIONS_SETTINGS = State()
NOTIFICATIONS_LIST = State()

# Report System States
REPORT_CREATE = State()
REPORT_DETAILS = State()
REPORT_STATUS = State()

# Guide System States
GUIDE_CREATE = State()
GUIDE_EDIT = State()
GUIDE_VIEW = State()
GUIDE_LIST = State()

# Analytics States
ANALYTICS_OVERVIEW = State()
ANALYTICS_DETAILED = State()
ANALYTICS_EXPORT = State()

# Screenshot Management States
SCREENSHOT_UPLOAD = State()
SCREENSHOT_REVIEW = State()

SCREENSHOT_GALLERY = State()

# Support States
SUPPORT_TICKET = State()
SUPPORT_CHAT = State()
SUPPORT_FAQ = State()
