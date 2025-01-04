from aiogram.fsm.state import StatesGroup, State

# Основне меню
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

# Турніри
class TournamentStates(StatesGroup):
    MENU = State()                          # 21. Меню турнірів
    CREATE_TOURNAMENT = State()             # 50. Створення турніру
    EDIT_TOURNAMENT = State()               # 51. Редагування турніру
    JOIN_TOURNAMENT = State()               # 52. Приєднання до турніру
    LIST_TOURNAMENTS = State()              # 53. Список турнірів
    BRACKET_TOURNAMENT = State()            # 54. Блок-діаграма турніру
    RESULTS_TOURNAMENT = State()            # 55. Результати турніру
    RULES_TOURNAMENT = State()              # 56. Правила турніру

# Управління турнірами
class TournamentManagementStates(StatesGroup):
    MENU_MANAGEMENT = State()               # Меню управління турнірами
    CREATE_MANAGEMENT_TOURNAMENT = State()  # 50. Створення турніру в контексті управління
    EDIT_MANAGEMENT_TOURNAMENT = State()    # 51. Редагування турніру в контексті управління
    JOIN_MANAGEMENT_TOURNAMENT = State()    # 52. Приєднання до турніру в контексті управління
    LIST_MANAGEMENT_TOURNAMENTS = State()   # 53. Список турнірів в контексті управління
    BRACKET_MANAGEMENT_TOURNAMENT = State() # 54. Блок-діаграма турніру в контексті управління
    RESULTS_MANAGEMENT_TOURNAMENT = State() # 55. Результати турніру в контексті управління
    RULES_MANAGEMENT_TOURNAMENT = State()   # 56. Правила турніру в контексті управління

# Герої
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

# Порівняння героїв
class ComparisonStates(StatesGroup):
    SELECT_FIRST_HERO = State()         # 33. Вибір першого героя для порівняння
    SELECT_SECOND_HERO = State()        # 34. Вибір другого героя для порівняння
    DISPLAY_RESULT = State()            # 35. Показ результатів порівняння

# Пошук
class SearchStates(StatesGroup):
    SEARCH_HERO = State()               # 36. Стан пошуку героя
    SEARCH_TOPIC = State()              # 44. Пошук за темою
    SEARCH_CATEGORY = State()           # 45. Пошук за категорією
    SEARCH_RESULT = State()             # 46. Результати пошуку
    SEARCH_FILTER = State()             # 47. Фільтрація пошуку
    SEARCH_HISTORY = State()            # 48. Історія пошуку
    SEARCH_FAVORITES = State()          # 49. Обрані пошукові запити

# Досягнення
class AchievementStates(StatesGroup):
    VIEW_ACHIEVEMENTS = State()         # 72. Перегляд досягнень
    ACHIEVEMENT_PROGRESS = State()      # 73. Прогрес досягнень
    CLAIM_ACHIEVEMENT = State()         # 74. Отримання досягнення

# Спільнота
class CommunityStates(StatesGroup):
    COMMUNITY_CHAT = State()            # 75. Чат спільноти
    COMMUNITY_EVENTS = State()          # 76. Події спільноти
    COMMUNITY_RULES = State()           # 77. Правила спільноти

# Сповіщення
class NotificationsStates(StatesGroup):
    NOTIFICATIONS_SETTINGS = State()     # 78. Налаштування сповіщень
    NOTIFICATIONS_LIST = State()         # 79. Список сповіщень

# Звіти
class ReportStates(StatesGroup):
    CREATE_REPORT = State()             # 80. Створення звіту
    REPORT_DETAILS = State()            # 81. Деталі звіту
    REPORT_STATUS = State()             # 82. Статус звіту

# Посібники
class GuideStates(StatesGroup):
    CREATE_GUIDE = State()              # 83. Створення посібника
    EDIT_GUIDE = State()                # 84. Редагування посібника
    VIEW_GUIDE = State()                # 85. Перегляд посібника
    LIST_GUIDES = State()                # 86. Список посібників

# Аналітика
class AnalyticsStates(StatesGroup):
    OVERVIEW_ANALYTICS = State()        # 87. Загальний огляд аналітики
    DETAILED_ANALYTICS = State()        # 88. Деталізована аналітика
    EXPORT_ANALYTICS = State()          # 89. Експорт аналітики

# Управління скріншотами
class ScreenshotStates(StatesGroup):
    UPLOAD_SCREENSHOT = State()         # 90. Завантаження скріншоту
    REVIEW_SCREENSHOT = State()         # 91. Рецензування скріншоту
    SCREENSHOT_GALLERY = State()        # 92. Галерея скріншотів

# Підтримка
class SupportStates(StatesGroup):
    SUPPORT_TICKET = State()            # 93. Квиток підтримки
    SUPPORT_CHAT = State()              # 94. Чат підтримки
    SUPPORT_FAQ = State()               # 95. Часті запитання підтримки

# Вступні сторінки
class IntroStates(StatesGroup):
    INTRO_PAGE_1 = State()               # 96. Перша сторінка вступу
    INTRO_PAGE_2 = State()               # 97. Друга сторінка вступу
    INTRO_PAGE_3 = State()               # 98. Третя сторінка вступу
    INTRO_COMPLETE = State()             # 99. Завершення вступу
