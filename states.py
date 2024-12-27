from aiogram.fsm.state import State, StatesGroup


class MenuStates(StatesGroup):
    # Основне меню
    MAIN_MENU = State()                 # Головне меню користувача
    CHALLENGES_MENU = State()           # Меню викликів
    GUIDES_MENU = State()               # Меню посібників
    BUST_MENU = State()                  # Меню BUST
    TEAMS_MENU = State()                # Меню команд
    TRADING_MENU = State()              # Меню торгівлі
    SETTINGS_MENU = State()             # Меню налаштувань
    SETTINGS_SUBMENU = State()          # Підменю налаштувань
    SELECT_LANGUAGE = State()           # Вибір мови
    PROFILE_MENU = State()              # Меню профілю
    STATS_MENU = State()                # Меню статистики
    ACHIEVEMENTS_MENU = State()         # Меню досягнень
    FEEDBACK_MENU = State()             # Меню зворотного зв'язку
    HELP_MENU = State()                 # Меню довідки
    MY_TEAM_MENU = State()              # Меню моєї команди
    GPT_MENU = State()                  # Меню GPT
    HELP_SUBMENU = State()              # Підменю довідки
    CHANGE_USERNAME = State()           # Зміна імені користувача
    RECEIVE_FEEDBACK = State()          # Отримання зворотного зв'язку
    REPORT_BUG = State()                # Повідомлення про помилку

    # Раніше запропоновані стани
    TOURNAMENTS_MENU = State()          # Меню турнірів
    HEROES_MENU = State()               # Меню героїв
    COUNTER_PICKS_MENU = State()        # Меню контрпічів
    BUILDS_MENU = State()                # Меню збірок
    VOTING_MENU = State()                # Меню голосування
    NAVIGATION_MENU = State()            # Меню навігації

    # Нові стани
    META_MENU = State()                  # Меню мета-ігри
    M6_MENU = State()                    # Меню секції M6

    # Додаткові стани, знайдені в обробниках
    HERO_LIST_MENU = State()             # Меню списку героїв у мета-меню
    RECOMMENDATIONS_MENU = State()       # Меню рекомендацій у мета-меню
    UPDATES_MENU = State()               # Меню оновлень у мета-меню
    BACK_TO_MAIN = State()               # Повернення до головного меню

    # Стани порівняння героїв
    COMPARISON_STEP_1 = State()          # Вибір першого героя/предмета для порівняння
    COMPARISON_STEP_2 = State()          # Вибір другого героя/предмета для порівняння
    COMPARISON_RESULT = State()          # Показ результатів порівняння

    # Стани пошуку та управління героями
    SEARCH_HERO = State()                # Стан пошуку героя
    HERO_DETAILS = State()               # Перегляд деталей героя
    HERO_SELECTION = State()             # Вибір героя зі списку
    HERO_FILTER = State()                # Фільтрація героїв
    HERO_SORT = State()                  # Сортування героїв
    HERO_FAVORITES = State()             # Обрані герої
    HERO_STATISTICS = State()            # Статистика героя

    # Стани системи пошуку
    SEARCH_TOPIC = State()               # Пошук за темою
    SEARCH_CATEGORY = State()            # Пошук за категорією
    SEARCH_RESULT = State()              # Результати пошуку
    SEARCH_FILTER = State()              # Фільтрація пошуку
    SEARCH_HISTORY = State()             # Історія пошуку
    SEARCH_FAVORITES = State()           # Обрані пошукові запити

    # Стани системи турнірів
    TOURNAMENT_CREATE = State()          # Створення турніру
    TOURNAMENT_EDIT = State()            # Редагування турніру
    TOURNAMENT_JOIN = State()            # Приєднання до турніру
    TOURNAMENT_LIST = State()            # Список турнірів
    TOURNAMENT_BRACKET = State()         # Блок-діаграма турніру
    TOURNAMENT_RESULTS = State()         # Результати турніру
    TOURNAMENT_RULES = State()           # Правила турніру

    # Стани управління командами
    TEAM_CREATE = State()                # Створення команди
    TEAM_EDIT = State()                  # Редагування команди
    TEAM_INVITE = State()                # Запрошення до команди
    TEAM_ROSTER = State()                # Список гравців команди
    TEAM_SETTINGS = State()              # Налаштування команди
    TEAM_STATS = State()                 # Статистика команди

    # Стани матчів
    MATCH_CREATE = State()               # Створення матчу
    MATCH_JOIN = State()                 # Приєднання до матчу
    MATCH_RESULT = State()               # Результат матчу
    MATCH_HISTORY = State()              # Історія матчів
    MATCH_REPORT = State()               # Звіт про матч

    # Стани управління контентом
    CONTENT_CREATE = State()             # Створення контенту
    CONTENT_EDIT = State()               # Редагування контенту
    CONTENT_DELETE = State()             # Видалення контенту
    CONTENT_REVIEW = State()             # Рецензування контенту

    # Стани системи досягнень
    ACHIEVEMENT_VIEW = State()           # Перегляд досягнень
    ACHIEVEMENT_PROGRESS = State()       # Прогрес досягнень
    ACHIEVEMENT_CLAIM = State()          # Отримання досягнення

    # Стани спільноти
    COMMUNITY_CHAT = State()             # Чат спільноти
    COMMUNITY_EVENTS = State()           # Події спільноти
    COMMUNITY_RULES = State()            # Правила спільноти

    # Стани сповіщень
    NOTIFICATIONS_SETTINGS = State()      # Налаштування сповіщень
    NOTIFICATIONS_LIST = State()          # Список сповіщень

    # Стани системи звітів
    REPORT_CREATE = State()              # Створення звіту
    REPORT_DETAILS = State()             # Деталі звіту
    REPORT_STATUS = State()              # Статус звіту

    # Стани системи посібників
    GUIDE_CREATE = State()               # Створення посібника
    GUIDE_EDIT = State()                 # Редагування посібника
    GUIDE_VIEW = State()                 # Перегляд посібника
    GUIDE_LIST = State()                 # Список посібників

    # Стани аналітики
    ANALYTICS_OVERVIEW = State()         # Загальний огляд аналітики
    ANALYTICS_DETAILED = State()         # Деталізована аналітика
    ANALYTICS_EXPORT = State()           # Експорт аналітики

    # Стани управління скріншотами
    SCREENSHOT_UPLOAD = State()          # Завантаження скріншоту
    SCREENSHOT_REVIEW = State()          # Рецензування скріншоту
    SCREENSHOT_GALLERY = State()         # Галерея скріншотів

    # Стани підтримки
    SUPPORT_TICKET = State()             # Квиток підтримки
    SUPPORT_CHAT = State()               # Чат підтримки
    SUPPORT_FAQ = State()                # Часті запитання підтримки

    # Intro states (додайте це до існуючих станів)
    INTRO_PAGE_1 = State()           # Перша сторінка вступу
    INTRO_PAGE_2 = State()           # Друга сторінка вступу
    INTRO_PAGE_3 = State()           # Третя сторінка вступу
    INTRO_COMPLETE = State()
