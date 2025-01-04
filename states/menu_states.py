from aiogram.fsm.state import StatesGroup, State


# 1-20: Основне меню
class MainMenuStates(StatesGroup):
    MAIN_MENU = State()                 # 1. Головне меню користувача
    CHALLENGES_MENU = State()           # 2. Меню викликів
    GUIDES_MENU = State()               # 3. Меню посібників
    BUST_MENU = State()                 # 4. Меню BUST
    TEAMS_MENU = State()                # 5. Меню команд
    TRADING_MENU = State()              # 6. Меню торгівлі
    SETTINGS_MENU = State()             # 7. Меню налаштувань
    SETTINGS_SUBMENU = State()          # 8. Підменю налаштувань
    SELECT_LANGUAGE = State()           # 9. Вибір мови
    HELP_MENU = State()                 # 14. Меню довідки
    HELP_SUBMENU = State()              # 17. Підменю довідки
    BACK_TO_MAIN = State()              # 32. Повернення до головного меню


# 21-26: Турніри та пов'язані стани
class TournamentStates(StatesGroup):
    TOURNAMENTS_MENU = State()          # 21. Меню турнірів
    TOURNAMENT_CREATE = State()         # 50. Створення турніру
    TOURNAMENT_EDIT = State()           # 51. Редагування турніру
    TOURNAMENT_JOIN = State()           # 52. Приєднання до турніру
    TOURNAMENT_LIST = State()           # 53. Список турнірів
    TOURNAMENT_BRACKET = State()        # 54. Блок-діаграма турніру
    TOURNAMENT_RESULTS = State()        # 55. Результати турніру
    TOURNAMENT_RULES = State()          # 56. Правила турніру


# 27-28: META та M6
class MetaM6States(StatesGroup):
    META_MENU = State()                 # 27. Меню мета-ігри
    M6_MENU = State()                   # 28. Меню секції M6


# 29-43: Герої та пов'язані стани
class HeroesStates(StatesGroup):
    HEROES_MENU = State()               # 22. Меню героїв
    HERO_LIST_MENU = State()            # 29. Меню списку героїв у мета-меню
    RECOMMENDATIONS_MENU = State()      # 30. Меню рекомендацій у мета-меню
    UPDATES_MENU = State()              # 31. Меню оновлень у мета-меню
    HERO_DETAILS = State()              # 37. Перегляд деталей героя
    HERO_SELECTION = State()            # 38. Вибір героя зі списку
    HERO_FILTER = State()               # 39. Фільтрація героїв
    HERO_SORT = State()                 # 40. Сортування героїв
    HERO_FAVORITES = State()            # 41. Обрані герої
    HERO_STATISTICS = State()           # 42. Статистика героя
    HERO_CLASS_MENU = State()           # 43. Меню класів героїв


# 33-35: Порівняння героїв
class ComparisonStates(StatesGroup):
    COMPARISON_STEP_1 = State()         # 33. Вибір першого героя/предмета для порівняння
    COMPARISON_STEP_2 = State()         # 34. Вибір другого героя/предмета для порівняння
    COMPARISON_RESULT = State()         # 35. Показ результатів порівняння


# 36-49: Пошук та управління героями
class SearchStates(StatesGroup):
    SEARCH_HERO = State()               # 36. Стан пошуку героя
    SEARCH_TOPIC = State()              # 44. Пошук за темою
    SEARCH_CATEGORY = State()           # 45. Пошук за категорією
    SEARCH_RESULT = State()             # 46. Результати пошуку
    SEARCH_FILTER = State()             # 47. Фільтрація пошуку
    SEARCH_HISTORY = State()            # 48. Історія пошуку
    SEARCH_FAVORITES = State()          # 49. Обрані пошукові запити


# 50-71: Турніри, команди, матчі та управління контентом
class TournamentManagementStates(StatesGroup):
    # Турніри
    TOURNAMENT_CREATE = State()         # 50. Створення турніру
    TOURNAMENT_EDIT = State()           # 51. Редагування турніру
    TOURNAMENT_JOIN = State()           # 52. Приєднання до турніру
    TOURNAMENT_LIST = State()           # 53. Список турнірів
    TOURNAMENT_BRACKET = State()        # 54. Блок-діаграма турніру
    TOURNAMENT_RESULTS = State()        # 55. Результати турніру
    TOURNAMENT_RULES = State()          # 56. Правила турніру

    # Команди
    TEAM_CREATE = State()               # 57. Створення команди
    TEAM_EDIT = State()                 # 58. Редагування команди
    TEAM_INVITE = State()               # 59. Запрошення до команди
    TEAM_ROSTER = State()               # 60. Список гравців команди
    TEAM_SETTINGS = State()             # 61. Налаштування команди
    TEAM_STATS = State()                # 62. Статистика команди

    # Матчі
    MATCH_CREATE = State()              # 63. Створення матчу
    MATCH_JOIN = State()                # 64. Приєднання до матчу
    MATCH_RESULT = State()              # 65. Результат матчу
    MATCH_HISTORY = State()             # 66. Історія матчів
    MATCH_REPORT = State()              # 67. Звіт про матч

    # Управління контентом
    CONTENT_CREATE = State()            # 68. Створення контенту
    CONTENT_EDIT = State()              # 69. Редагування контенту
    CONTENT_DELETE = State()            # 70. Видалення контенту
    CONTENT_REVIEW = State()            # 71. Рецензування контенту


# 72-74: Досягнення
class AchievementStates(StatesGroup):
    ACHIEVEMENT_VIEW = State()          # 72. Перегляд досягнень
    ACHIEVEMENT_PROGRESS = State()      # 73. Прогрес досягнень
    ACHIEVEMENT_CLAIM = State()         # 74. Отримання досягнення


# 75-77: Спільнота
class CommunityStates(StatesGroup):
    COMMUNITY_CHAT = State()            # 75. Чат спільноти
    COMMUNITY_EVENTS = State()          # 76. Події спільноти
    COMMUNITY_RULES = State()           # 77. Правила спільноти


# 78-79: Сповіщення
class NotificationsStates(StatesGroup):
    NOTIFICATIONS_SETTINGS = State()     # 78. Налаштування сповіщень
    NOTIFICATIONS_LIST = State()         # 79. Список сповіщень


# 80-82: Звіти
class ReportStates(StatesGroup):
    REPORT_CREATE = State()             # 80. Створення звіту
    REPORT_DETAILS = State()            # 81. Деталі звіту
    REPORT_STATUS = State()             # 82. Статус звіту


# 83-86: Посібники
class GuideStates(StatesGroup):
    GUIDE_CREATE = State()              # 83. Створення посібника
    GUIDE_EDIT = State()                # 84. Редагування посібника
    GUIDE_VIEW = State()                # 85. Перегляд посібника
    GUIDE_LIST = State()                # 86. Список посібників


# 87-89: Аналітика
class AnalyticsStates(StatesGroup):
    ANALYTICS_OVERVIEW = State()        # 87. Загальний огляд аналітики
    ANALYTICS_DETAILED = State()        # 88. Деталізована аналітика
    ANALYTICS_EXPORT = State()          # 89. Експорт аналітики


# 90-92: Управління скріншотами
class ScreenshotStates(StatesGroup):
    SCREENSHOT_UPLOAD = State()         # 90. Завантаження скріншоту
    SCREENSHOT_REVIEW = State()         # 91. Рецензування скріншоту
    SCREENSHOT_GALLERY = State()        # 92. Галерея скріншотів


# 93-95: Підтримка
class SupportStates(StatesGroup):
    SUPPORT_TICKET = State()            # 93. Квиток підтримки
    SUPPORT_CHAT = State()              # 94. Чат підтримки
    SUPPORT_FAQ = State()               # 95. Часті запитання підтримки


# 96-99: Вступні сторінки
class IntroStates(StatesGroup):
    INTRO_PAGE_1 = State()               # 96. Перша сторінка вступу
    INTRO_PAGE_2 = State()               # 97. Друга сторінка вступу
    INTRO_PAGE_3 = State()               # 98. Третя сторінка вступу
    INTRO_COMPLETE = State()             # 99. Завершення вступу
