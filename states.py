from aiogram.fsm.state import State, StatesGroup

# Основні меню
class MainMenuStates(StatesGroup):
    MAIN_MENU = State()                 # Головне меню користувача
    CHALLENGES_MENU = State()           # Меню викликів
    GUIDES_MENU = State()               # Меню посібників
    BUST_MENU = State()                 # Меню BUST
    TEAMS_MENU = State()                # Меню команд
    TRADING_MENU = State()              # Меню торгівлі
    SETTINGS_MENU = State()             # Меню налаштувань

# Пошук та фільтри
class SearchStates(StatesGroup):
    SEARCH_HERO = State()               # Пошук героя
    HERO_FILTER = State()               # Фільтрація героїв
    HERO_SORT = State()                 # Сортування героїв

# Турніри
class TournamentStates(StatesGroup):
    TOURNAMENT_CREATE = State()         # Створення турніру
    TOURNAMENT_EDIT = State()           # Редагування турніру
    TOURNAMENT_JOIN = State()           # Приєднання до турніру
    TOURNAMENT_RESULTS = State()        # Результати турніру

# Система досягнень
class AchievementStates(StatesGroup):
    ACHIEVEMENT_VIEW = State()          # Перегляд досягнень
    ACHIEVEMENT_PROGRESS = State()      # Прогрес досягнень
    ACHIEVEMENT_CLAIM = State()         # Отримання досягнення

# Intro
class IntroStates(StatesGroup):
    INTRO_PAGE_1 = State()              # Перша сторінка вступу
    INTRO_PAGE_2 = State()              # Друга сторінка вступу
    INTRO_PAGE_3 = State()              # Третя сторінка вступу
    INTRO_COMPLETE = State()            # Завершення вступу

# Інші стани
class MiscellaneousStates(StatesGroup):
    SUPPORT_CHAT = State()              # Чат підтримки
    SUPPORT_FAQ = State()               # Часті запитання підтримки
